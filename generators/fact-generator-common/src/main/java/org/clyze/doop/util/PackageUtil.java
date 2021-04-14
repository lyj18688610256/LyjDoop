package org.clyze.doop.util;

import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;
import org.apache.commons.collections4.Trie;
import org.apache.commons.collections4.trie.PatriciaTrie;
import org.apache.commons.io.FilenameUtils;
import org.clyze.doop.common.BytecodeUtil;
import org.clyze.utils.ContainerUtils;
import org.clyze.utils.JHelper;
import org.jf.dexlib2.dexbacked.DexBackedClassDef;
import org.jf.dexlib2.dexbacked.DexBackedDexFile;
import org.jf.dexlib2.iface.MultiDexContainer;

import static org.jf.dexlib2.DexFileFactory.loadDexContainer;

/** Computes the app-regex for JAR/APK/AAR inputs. */
public class PackageUtil {

	/** Debugging flag. */
	private static final boolean debug = false;

	/**
	 * Returns a set of the packages contained in the given JAR.
	 * Any classes that are not included in packages are also retrieved.
	 */
	public static Set<String> getPackages(File archive) throws IOException {
		Set<Regex> packages = new HashSet<>();
		String name = archive.getName().toLowerCase();
		if (name.endsWith(".jar") || name.endsWith(".zip"))
			packages = getPackagesForJAR(archive);
		else if (name.endsWith(".apk"))
			packages = getPackagesForAPK(archive);
		else if (name.endsWith(".aar"))
			packages = getPackagesForAAR(archive);
		else if (name.endsWith(".class"))
			packages = getPackagesForBytecode(archive);
		else
			System.err.println("Cannot compute packages, unknown file format: " + archive);
		return reducePackages(packages);
	}

	private static Set<String> reducePackages(Collection<Regex> packages) {
		Set<String> ret = new HashSet<>();
		Trie<String, Regex> trie = new PatriciaTrie<>();
		// Exact regular expressions are added to the return set, while prefix
		// expressions are put into a trie to be reduced.
		for (Regex r : packages)
			if (r.isWildcard)
				trie.put(r.text, r);
			else
				ret.add(r.toString());
		// Traverse regex entries and mark as 'deleted' the entries that are
		// covered by other prefixes.
		for (Map.Entry<String, Regex> regexEntry : trie.entrySet()) {
			String prefix = regexEntry.getKey();
			SortedMap<String, Regex> prefixMap = trie.prefixMap(prefix);
			// If this prefix matches many regex entries, keep only the entry
			// with this prefix.
			if (prefixMap.size() > 1)
				prefixMap.entrySet().stream().filter(entryToMark -> !prefix.equals(entryToMark.getKey()))
						.forEach(entryToMark -> entryToMark.getValue().deleted = true);
		}
		// Add regex entries, ignoring 'deleted' ones.
		for (Regex r : trie.values())
			if (!r.deleted)
				ret.add(r.toString());

		if (debug) {
			System.out.println("APP_REGEX: reduced " + packages.size() + " -> " + ret.size() + " entries");
			System.out.println("Original: " + packages);
			System.out.println("Reduced: " + ret);
		}

		return ret;
	}

	public static Set<Regex> getPackagesForBytecode(File f) throws IOException {
		return new HashSet<>(Collections.singletonList(getPackageFromDots(BytecodeUtil.getClassName(f))));
	}

	public static Set<Regex> getPackagesForAPK(File apk) throws IOException {
		Set<Regex> pkgs = new HashSet<>();
		MultiDexContainer<?> multiDex = loadDexContainer(apk, null);
		for (String dex : multiDex.getDexEntryNames()) {
			DexBackedDexFile dexFile = (DexBackedDexFile)multiDex.getEntry(dex).getDexFile();
			Set<? extends DexBackedClassDef> classes = dexFile.getClasses();
			for (DexBackedClassDef dexClass : classes) {
				String className = dexClass.toString();
				if (!className.startsWith("L") || !className.endsWith(";"))
					System.err.println("getPackagesForAPK: bad class " + className);
				else
					pkgs.add(getPackageFromSlashes(className.substring(1, className.length()-2)));
			}
		}
		return pkgs;
	}

	public static Regex getPackageFromSlashes(String s) {
		int idx = s.lastIndexOf('/');
		s = s.replaceAll("/", ".");
		return idx == -1 ? Regex.exact(s) : Regex.prefix(s.substring(0, idx));
	}

	public static Regex getPackageFromDots(String s) {
		int idx = s.lastIndexOf('.');
		return idx == -1 ? Regex.exact(s) : Regex.prefix(s.substring(0, idx));
	}

	public static Set<Regex> getPackagesForAAR(File aar) throws IOException {
		Set<Regex> ret = new HashSet<>();
		Set<String> tmpDirs = new HashSet<>();
		for (String jar : ContainerUtils.toJars(Collections.singletonList(aar.getCanonicalPath()), true, tmpDirs))
			ret.addAll(getPackagesForJAR(new File(jar)));
		JHelper.cleanUp(tmpDirs);
		return ret;
	}

	static Regex getPackageFromClassName(String className) {
		if (className.indexOf("/") > 0)
			return Regex.prefix(FilenameUtils.getPath(className).replace('/', '.'));
		else
			return Regex.exact(FilenameUtils.getBaseName(className));
	}

	static Set<Regex> getPackagesForJAR(File jar) throws IOException {
		ZipFile zip = new ZipFile(jar);
		Enumeration<? extends ZipEntry> entries = zip.entries();
		Set<Regex> packages = new HashSet<>();
		while (entries.hasMoreElements()) {
			final ZipEntry ze = entries.nextElement();
			if (ze.getName().endsWith(".class"))
				packages.add(getPackageFromClassName(ze.getName()));
		}
		return packages;
	}
}

/**
 * A regular exrpession that is either a constant piece of text or a wildcard-ending prefix.
 */
class Regex {
	/** The text part of the regular expression. */
	public final String text;
	/** If true, this is a wildcard-ending expression. */
	public final boolean isWildcard;
	/** Set to true during reduction. */
	public boolean deleted = false;

	private Regex(String text, boolean isWildcard) {
		this.text = text;
		this.isWildcard = isWildcard;
	}

	/**
	 * Create a regex matching an exact string.
	 * @param text   the string to match
	 * @return       the regex object
	 */
	static Regex exact(String text) {
		return new Regex(text, false);
	}

	/**
	 * Create a regex matching a string prefix.
	 * @param text   the string prefix to match
	 * @return       the regex object
	 */
	static Regex prefix(String text) {
		return new Regex(text, true);
	}

	@Override
	public String toString() {
		return isWildcard ? (text + ".*") : text;
	}
}