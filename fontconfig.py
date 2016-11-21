"""
A ctypes-based binding for the Fontconfig API, for Python
3.4 or later.
"""
#+
# Copyright 2016 by Lawrence D'Oliveiro <ldo@geek-central.gen.nz>.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library, in a file named COPYING; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA
#-

import ctypes as ct
from weakref import \
    WeakValueDictionary

fc = ct.cdll.LoadLibrary("libfontconfig.so.1")

libc = ct.cdll.LoadLibrary("libc.so.6")

class FC :
    "useful definitions from fontconfig/*.h. You will need to use the constants," \
    " but apart from that, see the more Pythonic wrappers defined outside this" \
    " class in preference to accessing low-level structures directly."

    Char8 = ct.c_ubyte
    Char16 = ct.c_ushort
    Char32 = ct.c_uint
    Bool = ct.c_int

    # Current Fontconfig version number
    MAJOR = 2
    MINOR = 11
    REVISION = 0
    VERSION = MAJOR * 10000 + MINOR * 100 + REVISION

    # Current font cache file format version
    CACHE_VERSION = "4"

    # pattern items
    FAMILY = "family" # String
    STYLE = "style" # String
    SLANT = "slant" # Int
    WEIGHT = "weight" # Int
    SIZE = "size" # Double
    ASPECT = "aspect" # Double
    PIXEL_SIZE = "pixelsize" # Double
    SPACING = "spacing" # Int
    FOUNDRY = "foundry" # String
    ANTIALIAS = "antialias" # Bool (depends)
    HINTING = "hinting" # Bool (true)
    HINT_STYLE = "hintstyle" # Int
    VERTICAL_LAYOUT = "verticallayout" # Bool (false)
    AUTOHINT = "autohint" # Bool (false)
    # FC_GLOBAL_ADVANCE is deprecated. this is simply ignored on freetype 2.4.5 or later
    GLOBAL_ADVANCE = "globaladvance" # Bool (true)
    WIDTH = "width" # Int
    FILE = "file" # String
    INDEX = "index" # Int
    FT_FACE = "ftface" # FT_Face
    RASTERIZER = "rasterizer" # String (deprecated)
    OUTLINE = "outline" # Bool
    SCALABLE = "scalable" # Bool
    SCALE = "scale" # double
    DPI = "dpi" # double
    RGBA = "rgba" # Int
    MINSPACE = "minspace" # Bool use minimum line spacing
    SOURCE = "source" # String (deprecated)
    CHARSET = "charset" # CharSet
    LANG = "lang" # String RFC 3066 langs
    FONTVERSION = "fontversion" # Int from 'head' table
    FULLNAME = "fullname" # String
    FAMILYLANG = "familylang" # String RFC 3066 langs
    STYLELANG = "stylelang" # String RFC 3066 langs
    FULLNAMELANG = "fullnamelang" # String RFC 3066 langs
    CAPABILITY = "capability" # String
    FONTFORMAT = "fontformat" # String
    EMBOLDEN = "embolden" # Bool - true if emboldening neede
    EMBEDDED_BITMAP = "embeddedbitmap" # Bool - true to enable embedded bitmaps
    DECORATIVE = "decorative" # Bool - true if style is a decorative variant
    LCD_FILTER = "lcdfilter" # Int
    FONT_FEATURES = "fontfeatures" # String
    NAMELANG = "namelang" # String RFC 3866 langs
    PRGNAME = "prgname" # String
    HASH = "hash" # String
    POSTSCRIPT_NAME = "postscriptname" # String

    CACHE_SUFFIX = ".cache-" + CACHE_VERSION
    DIR_CACHE_FILE = "fonts.cache-" + CACHE_VERSION
    USER_CACHE_FILE = ".fonts.cache-" + CACHE_VERSION

    # Adjust outline rasterizer
    CHAR_WIDTH = "charwidth" # Int
    CHAR_HEIGHT = "charheight" # Int
    MATRIX = "matrix" # FcMatrix

    WEIGHT_THIN = 0
    WEIGHT_EXTRALIGHT = 0
    WEIGHT_ULTRALIGHT = WEIGHT_EXTRALIGHT
    WEIGHT_LIGHT = 0
    WEIGHT_BOOK = 5
    WEIGHT_REGULAR = 0
    WEIGHT_NORMAL = WEIGHT_REGULAR
    WEIGHT_MEDIUM = 0
    WEIGHT_DEMIBOLD = 0
    WEIGHT_SEMIBOLD = WEIGHT_DEMIBOLD
    WEIGHT_BOLD = 0
    WEIGHT_EXTRABOLD = 5
    WEIGHT_ULTRABOLD = WEIGHT_EXTRABOLD
    WEIGHT_BLACK = 0
    WEIGHT_HEAVY = WEIGHT_BLACK
    WEIGHT_EXTRABLACK = 5
    WEIGHT_ULTRABLACK = WEIGHT_EXTRABLACK

    SLANT_ROMAN = 0
    SLANT_ITALIC = 0
    SLANT_OBLIQUE = 0

    WIDTH_ULTRACONDENSED = 0
    WIDTH_EXTRACONDENSED = 3
    WIDTH_CONDENSED = 5
    WIDTH_SEMICONDENSED = 7
    WIDTH_NORMAL = 0
    WIDTH_SEMIEXPANDED = 3
    WIDTH_EXPANDED = 5
    WIDTH_EXTRAEXPANDED = 0
    WIDTH_ULTRAEXPANDED = 0

    PROPORTIONAL = 0
    DUAL = 0
    MONO = 0
    CHARCELL = 0

    # sub-pixel order
    RGBA_UNKNOWN = 0
    RGBA_RGB = 1
    RGBA_BGR = 2
    RGBA_VRGB = 3
    RGBA_VBGR = 4
    RGBA_NONE = 5

    # hinting style
    HINT_NONE = 0
    HINT_SLIGHT = 1
    HINT_MEDIUM = 2
    HINT_FULL = 3

    # LCD filter
    LCD_NONE = 0
    LCD_DEFAULT = 1
    LCD_LIGHT = 2
    LCD_LEGACY = 3

    # enum FcType
    TypeUnknown = -1
    TypeVoid = 0
    TypeInteger = 1
    TypeDouble = 2
    TypeString = 3
    TypeBool = 4
    TypeMatrix = 5
    TypeCharSet = 6
    TypeFTFace = 7
    TypeLangSet = 8

    class Matrix(ct.Structure) :
        _fields_ = \
            [
                ("xx", ct.c_double),
                ("xy", ct.c_double),
                ("yx", ct.c_double),
                ("yy", ct.c_double),
            ]

        @classmethod
        def ident(celf) :
            "alternative to FcMatrixInit."
            return \
                celf(xx = 1, yy = 1, xy = 0, yx = 0)
        #end ident

    #end Matrix

    # TODO: FcObjectType, FcConstant

    # enum FcResult
    ResultMatch = 0
    ResultNoMatch = 1
    ResultTypeMismatch = 2
    FcResultNoId = 3
    FcResultOutOfMemory = 4

    class Value(ct.Structure) :
        pass
    #end Value
    class ValUnion(ct.Union) :
        pass
    #end ValUnion
    ValUnion._fields_ = \
        [
            ("s", ct.c_char_p),
            ("i", ct.c_int),
            ("b", Bool),
            ("d", ct.c_double),
            ("m", ct.POINTER(Matrix)),
            ("c", ct.c_void_p), # ct.POINTER(CharSet)
            ("f", ct.c_void_p), # ct.POINTER(FT_Face)
            ("l", ct.c_void_p), # ct.POINTER(LangSet)
        ]
    Value._fields_ = \
        [
            ("type", ct.c_uint), # Type
            ("u", ValUnion),
        ]
    del ValUnion

    class FontSet(ct.Structure) :
        _fields_ = \
            [
                ("nfont", ct.c_int), # number of used elements in array
                ("sfont", ct.c_int), # number of allocated elements in array
                ("fonts", ct.c_void_p), # array of pattern pointers
            ]
    #end FontSet
    FontSetPtr = ct.POINTER(FontSet)

    class ObjectSet(ct.Structure) :
        _fields_ = \
            [
                ("nobject", ct.c_int), # number of used elements in array
                ("sobject", ct.c_int), # number of allocated elements in array
                ("objects", ct.c_void_p), # array of pattern pointers
            ]
    #end ObjectSet
    ObjectSetPtr = ct.POINTER(ObjectSet)

    # enum FcMatchKind
    FcMatchPattern = 0
    FcMatchFont = 1
    FcMatchScan = 2

    # enum FcLangResult
    FcLangEqual = 0
    FcLangDifferentCountry = 1
    FcLangDifferentTerritory = 1
    FcLangDifferentLang = 2

    # enum FcSetName
    SetSystem = 0
    SetApplication = 1

    CHARSET_MAP_SIZE = 256 // 32
    CHARSET_DONE = 0xFFFFFFFF
    charset_page = Char32 * CHARSET_MAP_SIZE # array of bits

#end FC

#+
# Routine arg/result types
#-

fc.FcBlanksCreate.restype = ct.c_void_p
fc.FcBlanksCreate.argtypes = ()
fc.FcBlanksDestroy.restype = None
fc.FcBlanksDestroy.argtypes = (ct.c_void_p,)
fc.FcBlanksAdd.restype = FC.Bool
fc.FcBlanksAdd.argtypes = (ct.c_void_p, ct.c_uint)
fc.FcBlanksIsMember.restype = FC.Bool
fc.FcBlanksIsMember.argtypes = (ct.c_void_p, ct.c_uint)

# TODO: cache

fc.FcConfigHome.restype = ct.c_char_p
fc.FcConfigHome.argtypes = ()
fc.FcConfigEnableHome.restype = FC.Bool
fc.FcConfigEnableHome.argtypes = (FC.Bool,)
fc.FcConfigFilename.restype = ct.c_char_p
fc.FcConfigFilename.argtypes = (ct.c_char_p,)
fc.FcConfigCreate.restype = ct.c_void_p
fc.FcConfigCreate.argtypes = ()
fc.FcConfigReference.restype = ct.c_void_p
fc.FcConfigReference.argtypes = (ct.c_void_p,)
fc.FcConfigDestroy.restype = None
fc.FcConfigDestroy.argtypes = (ct.c_void_p,)
fc.FcConfigSetCurrent.restype = FC.Bool
fc.FcConfigSetCurrent.argtypes = (ct.c_void_p,)
fc.FcConfigGetCurrent.restype = ct.c_void_p
fc.FcConfigGetCurrent.argtypes = ()
fc.FcConfigUptoDate.restype = FC.Bool
fc.FcConfigUptoDate.argtypes = (ct.c_void_p,)
fc.FcConfigBuildFonts.restype = FC.Bool
fc.FcConfigBuildFonts.argtypes = (ct.c_void_p,)
fc.FcConfigGetFontDirs.restype = ct.c_void_p
fc.FcConfigGetFontDirs.argtypes = (ct.c_void_p,)
fc.FcConfigGetConfigDirs.restype = ct.c_void_p
fc.FcConfigGetConfigDirs.argtypes = (ct.c_void_p,)
fc.FcConfigGetConfigFiles.restype = ct.c_void_p
fc.FcConfigGetConfigFiles.argtypes = (ct.c_void_p,)
# fc.FcConfigGetCache -- deprecated
fc.FcConfigGetBlanks.restype = ct.c_void_p
fc.FcConfigGetBlanks.argtypes = (ct.c_void_p,)
fc.FcConfigGetCacheDirs.restype = ct.c_void_p
fc.FcConfigGetCacheDirs.argtypes = (ct.c_void_p,)
fc.FcConfigGetRescanInterval.restype = ct.c_int
fc.FcConfigGetRescanInterval.argtypes = (ct.c_void_p,)
fc.FcConfigSetRescanInterval.restype = FC.Bool
fc.FcConfigSetRescanInterval.argtypes = (ct.c_void_p,)
fc.FcConfigGetFonts.restype = ct.c_void_p
fc.FcConfigGetFonts.argtypes = (ct.c_void_p, ct.c_uint)
fc.FcConfigAppFontAddFile.restype = FC.Bool
fc.FcConfigAppFontAddFile.argtypes = (ct.c_void_p, ct.c_char_p)
fc.FcConfigAppFontAddDir.restype = FC.Bool
fc.FcConfigAppFontAddDir.argtypes = (ct.c_void_p, ct.c_char_p)
fc.FcConfigAppFontClear.restype = None
fc.FcConfigAppFontClear.argtypes = (ct.c_void_p,)
fc.FcConfigSubstituteWithPat.restype = FC.Bool
fc.FcConfigSubstituteWithPat.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_uint)
fc.FcConfigSubstitute.restype = FC.Bool
fc.FcConfigSubstitute.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_uint)
fc.FcConfigGetSysRoot.restype = ct.c_char_p
fc.FcConfigGetSysRoot.restype.argtypes = (ct.c_void_p,)
fc.FcConfigSetSysRoot.restype = None
fc.FcConfigSetSysRoot.argtypes = (ct.c_void_p, ct.c_char_p)

fc.FcCharSetCreate.restype = ct.c_void_p
fc.FcCharSetCreate.argtypes = ()
fc.FcCharSetDestroy.restype = None
fc.FcCharSetDestroy.argtypes = (ct.c_void_p,)
fc.FcCharSetAddChar.restype = FC.Bool
fc.FcCharSetAddChar.argtypes = (ct.c_void_p, FC.Char32)
fc.FcCharSetCount.restype = FC.Char32
fc.FcCharSetCount.argtypes = (ct.c_void_p,)
fc.FcCharSetFirstPage.restype = FC.Char32
fc.FcCharSetFirstPage.argtypes = (ct.c_void_p, ct.POINTER(FC.charset_page), ct.POINTER(FC.Char32))
fc.FcCharSetNextPage.restype = FC.Char32
fc.FcCharSetNextPage.argtypes = (ct.c_void_p, ct.POINTER(FC.charset_page), ct.POINTER(FC.Char32))

fc.FcGetDefaultLangs.restype = ct.c_void_p
fc.FcGetDefaultLangs.argtypes = ()
fc.FcDefaultSubstitute.restype = None
fc.FcDefaultSubstitute.argtypes = (ct.c_void_p,)

# TODO: print, file/dir

fc.FcFreeTypeQuery.restype = ct.c_void_p
fc.FcFreeTypeQuery.argtypes = (ct.c_char_p, ct.c_int, ct.c_void_p, ct.POINTER(ct.c_int))

fc.FcFontSetCreate.restype = ct.c_void_p
fc.FcFontSetCreate.argtypes = ()
fc.FcFontSetDestroy.restype = None
fc.FcFontSetDestroy.argtypes = (ct.c_void_p,)
fc.FcFontSetAdd.restype = FC.Bool
fc.FcFontSetAdd.argtypes = (ct.c_void_p, ct.c_void_p)

fc.FcInit.restype = FC.Bool
fc.FcInit.argtypes = ()
fc.FcFini.restype = None
fc.FcFini.argtypes = ()
fc.FcGetVersion.restype = ct.c_int
fc.FcGetVersion.argtypes = ()
fc.FcInitReinitialize.restype = FC.Bool
fc.FcInitReinitialize.argtypes = ()
fc.FcInitBringUptoDate.restype = FC.Bool
fc.FcInitBringUptoDate.argtypes = ()

fc.FcGetLangs.restype = ct.c_void_p
fc.FcGetLangs.argtypes = ()
fc.FcLangNormalize.restype = ct.c_void_p
fc.FcLangNormalize.argtypes = (ct.c_char_p,)
fc.FcLangGetCharSet.restype = ct.c_void_p
fc.FcLangGetCharSet.argtypes = (ct.c_char_p,)
fc.FcLangSetCreate.restype = ct.c_void_p
fc.FcLangSetCreate.argtypes = ()
fc.FcLangSetDestroy.restype = None
fc.FcLangSetDestroy.argtypes = (ct.c_void_p,)
fc.FcLangSetCopy.restype = ct.c_void_p
fc.FcLangSetCopy.argtypes = (ct.c_void_p,)
fc.FcLangSetAdd.restype = FC.Bool
fc.FcLangSetAdd.argtypes = (ct.c_void_p, ct.c_char_p)
fc.FcLangSetDel.restype = FC.Bool
fc.FcLangSetDel.argtypes = (ct.c_void_p, ct.c_char_p)
fc.FcLangSetHasLang.restype = ct.c_uint
fc.FcLangSetHasLang.argtypes = (ct.c_void_p, ct.c_char_p)
fc.FcLangSetCompare.restype = ct.c_uint
fc.FcLangSetCompare.argtypes = (ct.c_void_p, ct.c_void_p)
fc.FcLangSetContains.restype = FC.Bool
fc.FcLangSetContains.argtypes = (ct.c_void_p, ct.c_void_p)
fc.FcLangSetEqual.restype = FC.Bool
fc.FcLangSetEqual.argtypes = (ct.c_void_p, ct.c_void_p)
fc.FcLangSetHash.restype = ct.c_uint
fc.FcLangSetHash.argtypes = (ct.c_void_p,)
fc.FcLangSetGetLangs.restype = ct.c_void_p
fc.FcLangSetGetLangs.argtypes = (ct.c_void_p,)
fc.FcLangSetUnion.restype = ct.c_void_p
fc.FcLangSetUnion.argtypes = (ct.c_void_p, ct.c_void_p)
fc.FcLangSetSubtract.restype = ct.c_void_p
fc.FcLangSetSubtract.argtypes = (ct.c_void_p, ct.c_void_p)

fc.FcObjectSetCreate.restype = ct.c_void_p
fc.FcObjectSetCreate.argtypes = ()
fc.FcObjectSetAdd.restype = FC.Bool
fc.FcObjectSetAdd.argtypes = (ct.c_void_p, ct.c_char_p)
fc.FcObjectSetDestroy.restype = None
fc.FcObjectSetDestroy.argtypes = (ct.c_void_p,)
fc.FcFontSetList.restype = ct.c_void_p
fc.FcFontSetList.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_void_p, ct.c_void_p)
fc.FcFontList.restype = ct.c_void_p
fc.FcFontList.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)

# TODO: atomic, match

# probably don’t need rest of matrix stuff
fc.FcMatrixCopy.restype = ct.c_void_p
fc.FcMatrixCopy.argtypes = (ct.c_void_p,)

# TODO: name

# TODO: more pattern/value
fc.FcNameParse.restype = ct.c_void_p
fc.FcNameParse.argtypes = (ct.c_char_p,)
fc.FcNameUnparse.restype = ct.c_void_p
fc.FcNameUnparse.argtypes = (ct.c_void_p,)
fc.FcPatternCreate.restype = ct.c_void_p
fc.FcPatternCreate.argtypes = ()
fc.FcPatternDuplicate.restype = ct.c_void_p
fc.FcPatternDuplicate.argtypes = (ct.c_void_p,)
fc.FcPatternReference.restype = ct.c_void_p
fc.FcPatternReference.argtypes = (ct.c_void_p,)
fc.FcValueDestroy.restype = None
fc.FcValueDestroy.argtypes = (FC.Value,)
fc.FcValueSave.restype = FC.Value
fc.FcValueSave.argtypes = (FC.Value,)
fc.FcPatternDestroy.restype = None
fc.FcPatternDestroy.argtypes = (ct.c_void_p,)
fc.FcPatternFilter.restype = ct.c_void_p
fc.FcPatternFilter.argtypes = (ct.c_void_p, ct.c_void_p)

# probably don’t need rest of str/utf stuff
fc.FcStrCopy.restype = ct.c_char_p
fc.FcStrCopy.argtypes = (ct.c_void_p,)
fc.FcStrFree.restype = None
fc.FcStrFree.argtypes = (ct.c_void_p,)

# TODO: xml

fc.FcStrCopyFilename.restype = ct.c_char_p
fc.FcStrCopyFilename.argtypes = (ct.c_char_p,)

fc.FcStrSetCreate.restype = ct.c_void_p
fc.FcStrSetCreate.argtypes = ()
fc.FcStrSetAdd.restype = FC.Bool
fc.FcStrSetAdd.argtypes = (ct.c_void_p, ct.c_char_p)
# can’t (easily) use FcStrSetAddFilename, caller just has to use
# copy_filename (below) and add result to Python set of strings
fc.FcStrSetDestroy.restype = None
fc.FcStrSetDestroy.argtypes = (ct.c_void_p,)
fc.FcStrListCreate.restype = ct.c_void_p
fc.FcStrListCreate.argtypes = (ct.c_void_p,)
fc.FcStrListFirst.restype = None
fc.FcStrListFirst.argtypes = (ct.c_void_p,)
fc.FcStrListNext.restype = ct.c_char_p
fc.FcStrListNext.argtypes = (ct.c_void_p,)
fc.FcStrListDone.restype = None
fc.FcStrListDone.argtypes = (ct.c_void_p,)

libc.free.argtypes = (ct.c_void_p,)

class FontconfigError(Exception) :
    "just to identify a Fontconfig-specific error exception."

    def __init__(self, msg) :
        self.msg = msg
    #end __init__

#end FontconfigError

def init() :
    if fc.FcInit() == 0 :
        raise FontconfigError("FcInit failure")
    #end if
#end init

def reinitialize() :
    if fc.FcInitReinitialize() == 0 :
        raise FontconfigError("FcInitReinitialize failure")
    #end if
#end reinitialize

def init_bring_uptodate() :
    if fc.FcInitBringUptoDate() == 0 :
        raise FontconfigError("FcInitBringUptoDate failure")
    #end if
#end init_bring_uptodate

def fini() :
    fc.FcFini()
#end fini

def get_version() :
    return \
        fc.FcGetVersion()
#end get_version

def get_langs() :
    return \
        StrSet(fc.FcGetLangs()).from_fc()
#end get_langs

def lang_normalize(langname) :
    norm = fc.FcLangNormalize(langname.encode())
    if norm == None :
        raise FontconfigError("FcLangNormalize failure")
    #end if
    result = ct.cast(norm, ct.c_char_p).value.decode()
    fc.FcStrFree(norm)
    return \
        result
#end lang_normalize

class LangSet :
    "wrapper for FcLangSet objects. Do not instantiate directly: use the create, copy," \
    " union and difference methods."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
        )

    def __init__(self, _fcobj) :
        self._fcobj = _fcobj
    #end __init__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            fc.FcLangSetDestroy(self._fcobj)
            self._fcobj = None
        #end if
    #end __del__

    @classmethod
    def create(celf) :
        return \
            celf(fc.FcLangSetCreate())
    #end create

    def copy(self) :
        return \
            celf(fc.FcLangSetCopy(self._fcobj))
    #end copy

    def add(self, lang) :
        if fc.FcLangSetAdd(self._fcobj, lang.encode()) == 0 :
            raise FontconfigError("FcLangSetAdd failure")
        #end if
    #end add

    def remove(self, lang) :
        if fc.FcLangSetDel(self._fcobj, lang.encode()) == 0 :
            raise FontconfigError("FcLangSetDel failure")
        #end if
    #end remove

    def has(self, lang) :
        "returns one of FcLangEqual, FcLangDifferentCountry" \
        "/FcLangDifferentTerritory or FcLangDifferentLang."
        return \
            fc.FcLangSetHasLang(self._fcobj, lang.encode())
    #end has

    def compare(self, other) :
        "returns one of FcLangEqual, FcLangDifferentCountry" \
        "/FcLangDifferentTerritory or FcLangDifferentLang."
        if not isinstance(other, LangSet) :
            raise TypeError("other must also be a LangSet")
        #end if
        return \
            fc.FcLangSetCompare(self._fcobj, other._fcobj)
    #end compare

    def issuperset(self, other) :
        if not isinstance(other, LangSet) :
            raise TypeError("other must also be a LangSet")
        #end if
        return \
            fc.FcLangSetContains(self._fcobj, other._fcobj) != 0
    #end issuperset
    __ge__ = issuperset # allow ”>=” just like regular Python sets

    def __eq__(self, other) :
        if not isinstance(other, LangSet) :
            raise TypeError("other must also be a LangSet")
        #end if
        return \
            fc.FcLangSetEqual(self._fcobj, other._fcobj) != 0
    #end __eq__

    def hash(self) :
        return \
            fc.FcLangSetHash(self._fcobj)
    #end hash
    # __hash__ = hash # should I do this?

    @property
    def langs(self) :
        return \
            StrSet(fc.FcLangSetGetLangs(self._fcobj)).from_fc()
    #end langs

    # could I support __len__ in a roundabout way, by calling FcLangSetGetLangs
    # and getting the length of that?

    def union(self, other) :
        if not isinstance(other, LangSet) :
            raise TypeError("other must also be a LangSet")
        #end if
        return \
            type(self)(fc.FcLangSetUnion(self._fcobj, other._fcobj))
    #end union
    __or__ = union

    def difference(self, other) :
        if not isinstance(other, LangSet) :
            raise TypeError("other must also be a LangSet")
        #end if
        return \
            type(self)(fc.FcLangSetSubtract(self._fcobj, other._fcobj))
    #end difference
    __sub__ = difference

#end LangSet

class ObjectSet :
    "wrapper around FcObjectSet objects. For internal use only: all relevant" \
    " functions will pass and return Python sequences."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
        )

    def __init__(self, _fcobj) :
        self._fcobj = _fcobj
    #end __init__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            fc.FcObjectSetDestroy(self._fcobj)
            self._fcobj = None
        #end if
    #end __del__

    @classmethod
    def to_fc(celf, pyset) :
        result = fc.FcObjectSetCreate()
        for s in pyset :
            fc.FcObjectSetAdd(result, s.encode())
        #end for
        return \
            celf(result)
    #end to_fc

    def each(self) :
        f = ct.cast(self._fcobj, ct.POINTER(FC.ObjectSet))
        strs = ct.cast(f[0].objects, ct.POINTER(ct.c_void_p))
        for i in range(f[0].nobject) :
            yield ct.cast(strs[i], ct.c_char_p).value.decode()
        #end for
    #end each

    def from_fc(self) :
        return \
            tuple(self.each())
    #end from_fc

#end ObjectSet

class Blanks :
    "wrapper for FcBlanks objects. Do not instantiate directly: use the create method.\n" \
    "\n" \
    "Note the methods available are very limited, e.g. no enumeration of members or" \
    " determination of cardinality."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
            "_created",
            "__weakref__",
        )

    _instances = WeakValueDictionary()

    def __new__(celf, _fcobj, _created) :
        self = celf._instances.get(_fcobj)
        if self == None :
            self = super().__new__(celf)
            self._fcobj = _fcobj
            self._created = _created
            celf._instances[_fcobj] = self
        else :
            assert self._created == _created
        #end if
        return \
            self
    #end __new__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            if self._created :
                fc.FcBlanksDestroy(self._fcobj)
            #end if
            self._fcobj = None
        #end if
    #end __del__

    @classmethod
    def create(celf) :
        return \
            celf(fc.FcBlanksCreate(), True)
    #end create

    def add(self, elt) :
        if fc.FcBlanksAdd(self._fcobj, elt) == 0 :
            raise FontconfigError("FcBlanksAdd failure")
        #end if
    #end add

    def __contains__(self, elt) :
        return \
            fc.FcBlanksIsMember(self._fcobj, elt) != 0
    #end __contains__

#end Blanks

class Config :
    "high-level wrapper around FcConfig objects. Do not instantiate directly;" \
    " use the create method."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
            "__weakref__",
        )

    _instances = WeakValueDictionary()

    def __new__(celf, _fcobj) :
        self = celf._instances.get(_fcobj)
        if self == None :
            self = super().__new__(celf)
            self._fcobj = _fcobj
            celf._instances[_fcobj] = self
        else :
            fc.FcConfigDestroy(self._fcobj)
              # lose extra reference created by caller
        #end if
        return \
            self
    #end __new__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            fc.FcConfigDestroy(self._fcobj)
            self._fcobj = None
        #end if
    #end __del__

    @staticmethod
    def home() :
        return \
            fc.FcConfigHome().decode() # automatically stops at NUL?
    #end home

    @staticmethod
    def enable_home(enable) :
        return \
            fc.FcConfigEnableHome(int(enable)) != 0
    #end enable_home

    @staticmethod
    def file_name(name) :
        return \
            fc.FcConfigFilename(name.encode()).decode() # automatically stops at NUL?
    #end file_name

    @classmethod
    def create(celf) :
        return \
            celf(fc.FcConfigCreate())
    #end create

    def set_current(self) :
        if fc.FcConfigSetCurrent(self._fcobj) == 0 :
            raise FontconfigError("FcConfigSetCurrent failure")
        #end if
    #end set_current

    @classmethod
    def get_current(celf) :
        return \
            celf(fc.FcConfigReference(fc.FcConfigGetCurrent()))
    #end get_current

    @property
    def uptodate(self) :
        return \
            fc.FcConfigUptoDate(self._fcobj) != 0
    #end uptodate

    def build_fonts(self) :
        if fc.FcConfigBuildFonts(self._fcobj) == 0 :
            raise FontconfigError("FcConfigBuildFonts failure")
        #end if
    #end build_fonts

    @property
    def font_dirs(self) :
        return \
            StrList(fc.FcConfigGetFontDirs(self._fcobj)).from_fc()
    #end font_dirs

    @property
    def config_dirs(self) :
        return \
            StrList(fc.FcConfigGetConfigDirs(self._fcobj)).from_fc()
    #end config_dirs

    @property
    def config_files(self) :
        return \
            StrList(fc.FcConfigGetConfigFiles(self._fcobj)).from_fc()
    #end config_files

    @property
    def blanks(self) :
        return \
            Blanks(fc.FcConfigGetBlanks(self._fcobj, False))
    #end blanks

    @property
    def cache_dirs(self) :
        return \
            StrList(fc.FcConfigGetCacheDirs(self._fcobj)).from_fc()
    #end cache_dirs

    @property
    def rescan_interval(self) :
        return \
            fc.FcConfigGetRescanInterval(self._fcobj)
    #end rescan_interval

    @rescan_interval.setter
    def rescan_interval(self, interval) :
        if fc.FcConfigSetRescanInterval(self._fcobj, interval) == 0 :
            raise FontconfigError("FcConfigSetRescanInterval failure")
        #end if
    #end rescan_interval

    def get_fonts(self, set_name) :
        "returns one of the two sets of fonts, where set_name is either FC.SetSystem" \
        " or FC.SetApplication."
        fontset = fc.FcConfigGetFonts(self._fcobj, set_name)
        if fontset != None :
            result = FontSet(fontset, False).from_fc()
        else :
            result = ()
        #end if
        return \
            result
    #end get_fonts

    def app_font_add_file(self, filename) :
        if fc.FcConfigAppFontAddFile(self._fcobj, filename.encode()) == 0 :
            raise FontconfigError("FcConfigAppFontAddFile failure")
        #end if
    #end app_font_add_file

    def app_font_add_dir(self, dirname) :
        if fc.FcConfigAppFontAddDir(self._fcobj, dirname.encode()) == 0 :
            raise FontconfigError("FcConfigAppFontAddDir failure")
        #end if
    #end app_font_add_dir

    def app_font_clear(self) :
        fc.FcConfigAppFontClear(self._fcobj)
    #end app_font_clear

    def substitute_with_pat(self, p, p_pat, kind) :
        "kind must be FC.FcMatchPattern, FC.FcMatchFont or FC.FcMatchScan."
        if not isinstance(p, Pattern) or not isinstance(p_pat, Pattern) :
            raise TypeError("second and third args must be Patterns")
        #end if
        if fc.FcConfigSubstituteWithPat(self._fcobj, p._fcobj, p_pat._fcobj, kind) == 0 :
            raise FontconfigError("FcConfigSubstituteWithPat failure")
        #end if
    #end substitute_with_pat

    def substitute(self, p, kind) :
        "kind must be FC.FcMatchPattern, FC.FcMatchFont or FC.FcMatchScan."
        if not isinstance(p, Pattern) :
            raise TypeError("second arg must be Pattern")
        #end if
        if fc.FcConfigSubstitute(self._fcobj, p._fcobj, kind) == 0 :
            raise FontconfigError("FcConfigSubstitute failure")
        #end if
    #end substitute

    @property
    def sysroot(self) :
        result = fc.FcConfigGetSysRoot(self._fcobj)
        if bool(result) :
            result = result.decode()
        else :
            result = None
        #end if
        return \
            result
    #end sysroot

    @sysroot.setter
    def sysroot(self, newroot) :
        fc.FcConfigSetSysRoot(self._fcobj, newroot.encode())
    #end sysroot

    def font_set_list(self, sets, pat, props) :
        if not isinstance(pat, Pattern) :
            raise TypeError("pat must be a pattern")
        #end if
        nr_sets = len(sets)
        f_sets = tuple(FontSet.to_fc(s) for s in sets)
        c_sets = (ct.c_void_p * nr_sets)(s._fcobj for s in f_sets)
        fs = FontSet.to_fc(props)
        result = fc.FcFontSetList \
          (
            self._fcobj,
            ct.cast(c_sets, ct.c_void_p),
            nr_sets,
            pat._fcobj,
            ct.fs._fcobj
          )
        return \
            FontSet(result, True).from_fc()
    #end font_set_list

    def font_list(self, pat, props) :
        "finds all fonts matching Pattern pat, and returns a tuple of" \
        " Patterns describing them, containing only the properties named" \
        " in props."
        if not isinstance(pat, Pattern) :
            raise TypeError("pat must be a pattern")
        #end if
        fs = FontSet.to_fc(props)
        result = fc.FcFontList(self._fcobj, pat._fcobj, fs._fcobj)
        return \
            FontSet(result, True).from_fc()
    #end font_list

#end Config

class CharSet :
    "wrapper around FcCharSet objects. For internal use only: all relevant" \
    " functions will pass and return Python sequences."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
        )

    def __init__(self, _fcobj) :
        self._fcobj = _fcobj
    #end __init__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            fc.FcCharSetDestroy(self._fcobj)
            self._fcobj = None
        #end if
    #end __del__

    @classmethod
    def to_fc(celf, pyset) :
        result = fc.FcCharSetCreate()
        for char in pyset :
            fc.FcCharSetAddChar(result, char)
        #end for
        return \
            celf(result)
    #end to_fc

    def from_fc(self) :
        result = set()
        page = FC.charset_page()
        retrieve = fc.FcCharSetFirstPage
        next = FC.Char32()
        while True :
            base = retrieve(self._fcobj, ct.byref(page), ct.byref(next))
            if base == FC.CHARSET_DONE :
                break
            for i in range(len(page)) :
                for j in range(32) :
                    if 1 << j & page[i] != 0 :
                        result.add(base + i * 32 + j)
                    #end if
                #end for
            #end for
            if next == FC.CHARSET_DONE :
                break
            retrieve = fc.FcCharSetNextPage
        #end while
        return \
            result
    #end from_fc

#end CharSet

def copy_filename(s) :
    result = fc.FcStrCopyFilename(s.encode())
    if not bool(result) :
        raise FontconfigError("FcStrCopyFilename failure")
    #end if
    return \
        result.decode() # automatically stops at NUL?
#end copy_filename

def get_default_langs() :
    return \
        StrSet(fc.FcGetDefaultLangs()).from_fc()
#end get_default_langs

class FontSet :
    "wrapper around FcFontSet objects. For internal use only: all relevant" \
    " functions will pass and return Python sequences."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
            "_created",
            "__weakref__",
        )

    _instances = WeakValueDictionary()

    def __new__(celf, _fcobj, _created) :
        self = celf._instances.get(_fcobj)
        if self == None :
            self = super().__new__(celf)
            self._fcobj = _fcobj
            self._created = _created
            celf._instances[_fcobj] = self
        else :
            assert self._created == _created
        #end if
        return \
            self
    #end __new__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            if self._created :
                fc.FcFontSetDestroy(self._fcobj)
            #end if
            self._fcobj = None
        #end if
    #end __del__

    @classmethod
    def create(celf) :
        return \
            celf(fc.FcFontSetCreate(), True)
    #end create

    @classmethod
    def to_fc(celf, patset) :
        result = celf.create()
        for pat in patset :
            if not isinstance(pat, Pattern) :
                raise TypeError("element of patset is not a Pattern")
            #end if
            if fc.FcFontSetAdd(result._fcobj, pat._fcobj) == 0 :
                raise FontconfigError("FcFontSetAdd failure")
            #end if
        #end for
        return \
            result
    #end to_fc

    def each(self) :
        f = ct.cast(self._fcobj, ct.POINTER(FC.FontSet))
        pats = ct.cast(f[0].fonts, ct.POINTER(ct.c_void_p))
        for i in range(f[0].nfont) :
            yield Pattern(pats[i])
        #end for
    #end each

    def from_fc(self) :
        return \
            tuple(self.each())
    #end from_fc

#end FontSet

class Matrix :
    "Python represention of FcMatrix objects."

    __slots__ = ("xx", "xy", "yx", "yy") # to forestall typos

    @classmethod
    def from_fc(celf, m) :
        return \
            celf(xx = m.xx, xy = m.xy, yx = m.yx, yy = m.yy)
    #end from_fc

    def to_fc(m) :
        return \
            FC.Matrix(xx = m.xx, xy = m.xy, yx = m.yx, yy = m.yy)
    #end to_fc

#end Matrix

class Value :
    "wrapper around FcValue objects. For internal use only: all relevant" \
    " functions will pass and return regular Python objects."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
        )

    def __init__(self, _fcobj) :
        self._fcobj = _fcobj
    #end __init__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            fc.FcValueDestroy(self._fcobj)
            self._fcobj = None
        #end if
    #end __del__

    conv_from_fc = \
        {
            FC.TypeInteger : lambda v : int(v.i),
            FC.TypeDouble : lambda v : float(v.d),
            FC.TypeString : lambda v : v.s.value.decode(),
            FC.TypeBool : lambda v : v.b != 0,
            FC.TypeMatrix : lambda v : Matrix.from_fc(v.m.contents),
            FC.TypeCharSet : lambda v : CharSet(v.c).from_fc(),
            FC.TypeFTFace : lambda v : v.f, # leave as c_void_p for now
            FC.TypeLangSet : lambda v : LangSet(v.l).from_fc(),
        }

    conv_to_fc = \
        {
            int : (FC.TypeInteger, "i", lambda x : x),
            float : (FC.TypeDouble, "d", lambda x : x),
            str : (FC.TypeString, "s", lambda s : fc.FcStrCopy(s.encode())),
              # allocates memory!
            bool : (FC.TypeBool, "b", int),
            Matrix : (FC.TypeMatrix, "m", lambda m : fc.FcMatrixCopy(ct.byref(m.to_fc()))),
              # allocates memory!
            CharSet : (FC.TypeCharSet, "c", lambda s : CharSet.to_fc(s)),
              # allocates memory!
            # FTFace handled specially
            LangSet : (FC.TypeLangSet, "l", lambda l : l._fcobj),
        }

    @classmethod
    def from_fc(celf, v) :
        if v.type not in celf.conv_from_fc :
            raise TypeError("cannot convert FC.Value type %d" % v.type)
        #end if
        return \
            celf.conv_from_fc[v.type](v.u)
    #end from_fc

    @classmethod
    def to_fc(celf, x) :
        if type(x) not in celf.conv_to_fc :
            raise TypeError("cannot convert %s type to FC.Value" % type(x).__name__)
        #end if
        conv = celf.conv_to_fc(type(x))
        result = FC.Value()
        result.type = conv[0]
        setattr(result.u, conv[1], conv[2](x))
        return \
            celf(result)
    #end to_fc

#end Value

class Pattern :
    "wrapper around FcPattern objects. Do not instantiate directly; use create" \
    " method."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
            "__weakref__",
        )

    _instances = WeakValueDictionary()

    def __new__(celf, _fcobj) :
        self = celf._instances.get(_fcobj)
        if self == None :
            self = super().__new__(celf)
            self._fcobj = _fcobj
            celf._instances[_fcobj] = self
        else :
            fc.FcPatternDestroy(self._fcobj)
              # lose extra reference created by caller
        #end if
        return \
            self
    #end __new__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            fc.FcPatternDestroy(self._fcobj)
            self._fcobj = None
        #end if
    #end __del__

    @classmethod
    def create(celf) :
        return \
            celf(fc.FcPatternCreate())
    #end create

    @classmethod
    def freetype_query(celf, filename, id, blanks) :
        if blanks != None and not isinstance(blanks, Blanks) :
            raise TypeError("blanks must be a Blanks")
        #end if
        count = ct.c_int()
        pat = fc.FcFreeTypeQuery \
          (
            filename.encode(),
            id,
            (lambda : None, lambda : blanks._fcobj)[blanks != None](),
            ct.byref(count)
          )
        return \
            (celf(pat), count.value)
    #end freetype_query

    def duplicate(self) :
        return \
            type(self)(fc.FcPatternDuplicate(self._fcobj))
    #end duplicate

    def default_substitute(self) :
        fc.FcDefaultSubstitute(self._fcobj)
    #end default_substitute

    @classmethod
    def name_parse(celf, name) :
        return \
            celf(fc.FcNameParse(name.encode()))
    #end name_parse

    def name_unparse(self) :
        name = fc.FcNameUnparse(self._fcobj)
        result = ct.cast(name, ct.c_char_p).value.decode()
        libc.free(name)
        return \
            result
    #end name_unparse

    def filter(self, props) :
        os = ObjectSet.to_fc(props)
        result = fc.FcPatternFilter(self._fcobj, os._fcobj)
        return \
            type(self)(result)
    #end filter

    # TODO: rest of methods

#end Pattern

class StrSet :
    "wrapper around FcStrSet objects. For internal use only: all relevant" \
    " functions will pass and return Python sets."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
        )

    def __init__(self, _fcobj) :
        self._fcobj = _fcobj
    #end __init__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            fc.FcStrSetDestroy(self._fcobj)
            self._fcobj = None
        #end if
    #end __del__

    @classmethod
    def to_fc(celf, pyset) :
        result = fc.FcStrSetCreate()
        if result == None :
            raise FontconfigError("FcStrSetCreate failure")
        #end if
        for s in pyset :
            if fc.FcStrSetAdd(result, s) == 0 :
                raise FontconfigError("FcStrSetAdd failure")
            #end if
        #end for
        return \
            celf(result)
    #end to_fc

    def from_fc(self) :
        return \
            set(StrList.create(self).each())
    #end from_fc

#end StrSet

class StrList :
    "wrapper around FcStrList objects. For internal use only: all relevant" \
    " functions will pass and return sequences of Python strings."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
        )

    def __init__(self, _fcobj) :
        self._fcobj = _fcobj
    #end __init__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            fc.FcStrListDone(self._fcobj)
            self._fcobj = None
        #end if
    #end __del__

    @classmethod
    def create(celf, strset) :
        return \
            celf(fc.FcStrListCreate(strset._fcobj))
    #end create

    def each(self) :
        "yields each string in the list in turn."
        fc.FcStrListFirst(self._fcobj)
        while True :
            s = fc.FcStrListNext(self._fcobj)
            if s == None :
                break
            yield s.decode()
        #end while
    #end each

    def from_fc(self) :
        return \
            tuple(self.each())
    #end from_fc

#end StrList
