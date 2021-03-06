"""
A ctypes-based binding for the Fontconfig API, for Python
3.4 or later.
"""
#+
# Copyright 2016, 2018 by Lawrence D'Oliveiro <ldo@geek-central.gen.nz>.
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

import enum
import ctypes as ct
from weakref import \
    WeakValueDictionary
try :
    import freetype2 as freetype
except ImportError :
    freetype = None
#end try

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
    # GLOBAL_ADVANCE is deprecated. this is simply ignored on freetype 2.4.5 or later
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
    EMBOLDEN = "embolden" # Bool - true if emboldening needed
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
    WEIGHT_EXTRALIGHT = 40
    WEIGHT_ULTRALIGHT = WEIGHT_EXTRALIGHT
    WEIGHT_LIGHT = 50
    WEIGHT_DEMILIGHT = 55
    WEIGHT_SEMILIGHT = WEIGHT_DEMILIGHT
    WEIGHT_BOOK = 75
    WEIGHT_REGULAR = 80
    WEIGHT_NORMAL = WEIGHT_REGULAR
    WEIGHT_MEDIUM = 100
    WEIGHT_DEMIBOLD = 180
    WEIGHT_SEMIBOLD = WEIGHT_DEMIBOLD
    WEIGHT_BOLD = 200
    WEIGHT_EXTRABOLD = 205
    WEIGHT_ULTRABOLD = WEIGHT_EXTRABOLD
    WEIGHT_BLACK = 210
    WEIGHT_HEAVY = WEIGHT_BLACK
    WEIGHT_EXTRABLACK = 215
    WEIGHT_ULTRABLACK = WEIGHT_EXTRABLACK

    SLANT_ROMAN = 0
    SLANT_ITALIC = 100
    SLANT_OBLIQUE = 110

    WIDTH_ULTRACONDENSED = 50
    WIDTH_EXTRACONDENSED = 63
    WIDTH_CONDENSED = 75
    WIDTH_SEMICONDENSED = 87
    WIDTH_NORMAL = 100
    WIDTH_SEMIEXPANDED = 113
    WIDTH_EXPANDED = 125
    WIDTH_EXTRAEXPANDED = 150
    WIDTH_ULTRAEXPANDED = 200

    PROPORTIONAL = 0
    DUAL = 90
    MONO = 100
    CHARCELL = 110

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

    # FcObjectType, FcConstant -- deprecated?

    # enum FcResult
    ResultMatch = 0
    ResultNoMatch = 1
    ResultTypeMismatch = 2
    ResultNoId = 3
    ResultOutOfMemory = 4

    # NOTE: I cannot seem to make Fontconfig calls that take Value
    # objects without stack-smashing crashes. Seems there is something
    # not right in how ctypes passes these structures by value.
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
    MatchPattern = 0
    MatchFont = 1
    MatchScan = 2

    # enum FcLangResult
    LangEqual = 0
    LangDifferentCountry = 1
    LangDifferentTerritory = 1
    LangDifferentLang = 2

    # enum FcSetName
    SetSystem = 0
    SetApplication = 1

    CHARSET_MAP_SIZE = 256 // 32
    CHARSET_DONE = 0xFFFFFFFF
    charset_page = Char32 * CHARSET_MAP_SIZE # array of bits

#end FC

@enum.unique
class PROP(enum.Enum) :
    "all the recognized property names."
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
    # GLOBAL_ADVANCE is deprecated. this is simply ignored on freetype 2.4.5 or later
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
    EMBOLDEN = "embolden" # Bool - true if emboldening needed
    EMBEDDED_BITMAP = "embeddedbitmap" # Bool - true to enable embedded bitmaps
    DECORATIVE = "decorative" # Bool - true if style is a decorative variant
    LCD_FILTER = "lcdfilter" # Int
    FONT_FEATURES = "fontfeatures" # String
    NAMELANG = "namelang" # String RFC 3866 langs
    PRGNAME = "prgname" # String
    HASH = "hash" # String
    POSTSCRIPT_NAME = "postscriptname" # String

    @classmethod
    def ensure_prop(celf, name) :
        "name can be a PROP or a string, always returns a PROP."
        if not isinstance(name, celf) :
            name = celf.prop[name]
        #end if
        return \
            name
    #end ensure_prop

    @classmethod
    def ensure_str(celf, name) :
        "name can be a PROP or a string, always returns a string."
        if isinstance(name, celf) :
            name = name.value
        #end if
        return \
            name
    #end ensure_str

    @property
    def type(self) :
        return \
            {
                PROP.FAMILY : str,
                PROP.STYLE : str,
                PROP.SLANT : int,
                PROP.WEIGHT : int,
                PROP.SIZE : float,
                PROP.ASPECT : float,
                PROP.PIXEL_SIZE : float,
                PROP.SPACING : int,
                PROP.FOUNDRY : str,
                PROP.ANTIALIAS : bool,
                PROP.HINTING : bool,
                PROP.HINT_STYLE : int,
                PROP.VERTICAL_LAYOUT : bool,
                PROP.AUTOHINT : bool,
                # GLOBAL_ADVANCE is deprecated. this is simply ignored on freetype 2.4.5 or later
                PROP.GLOBAL_ADVANCE : bool,
                PROP.WIDTH : int,
                PROP.FILE : str,
                PROP.INDEX : int,
                PROP.FT_FACE : (lambda : None, lambda : freetype.face)[freetype != None](),
                PROP.RASTERIZER : str, # (deprecated)
                PROP.OUTLINE : bool,
                PROP.SCALABLE : bool,
                PROP.SCALE : float,
                PROP.DPI : float,
                PROP.RGBA : int,
                PROP.MINSPACE : bool,
                PROP.SOURCE : str, # (deprecated)
                PROP.CHARSET : set,
                PROP.LANG : str,
                PROP.FONTVERSION : int,
                PROP.FULLNAME : str,
                PROP.FAMILYLANG : str,
                PROP.STYLELANG : str,
                PROP.FULLNAMELANG : str,
                PROP.CAPABILITY : str,
                PROP.FONTFORMAT : str,
                PROP.EMBOLDEN : bool,
                PROP.EMBEDDED_BITMAP : bool,
                PROP.DECORATIVE : bool,
                PROP.LCD_FILTER : int,
                PROP.FONT_FEATURES : str,
                PROP.NAMELANG : str,
                PROP.PRGNAME : str,
                PROP.HASH : str,
                PROP.POSTSCRIPT_NAME : str,
            }[self]
    #end type

    @property
    def fc_type(self) :
        return \
            {
                PROP.FAMILY : FC.TypeString,
                PROP.STYLE : FC.TypeString,
                PROP.SLANT : FC.TypeInteger,
                PROP.WEIGHT : FC.TypeInteger,
                PROP.SIZE : FC.TypeDouble,
                PROP.ASPECT : FC.TypeDouble,
                PROP.PIXEL_SIZE : FC.TypeDouble,
                PROP.SPACING : FC.TypeInteger,
                PROP.FOUNDRY : FC.TypeString,
                PROP.ANTIALIAS : FC.TypeBool,
                PROP.HINTING : FC.TypeBool,
                PROP.HINT_STYLE : FC.TypeInteger,
                PROP.VERTICAL_LAYOUT : FC.TypeBool,
                PROP.AUTOHINT : FC.TypeBool,
                # GLOBAL_ADVANCE is deprecated. this is simply ignored on freetype 2.4.5 or later
                PROP.GLOBAL_ADVANCE : FC.TypeBool,
                PROP.WIDTH : FC.TypeInteger,
                PROP.FILE : FC.TypeString,
                PROP.INDEX : FC.TypeInteger,
                PROP.FT_FACE : FC.TypeFTFace,
                PROP.RASTERIZER : FC.TypeString, # (deprecated)
                PROP.OUTLINE : FC.TypeBool,
                PROP.SCALABLE : FC.TypeBool,
                PROP.SCALE : FC.TypeDouble,
                PROP.DPI : FC.TypeDouble,
                PROP.RGBA : FC.TypeInteger,
                PROP.MINSPACE : FC.TypeBool,
                PROP.SOURCE : FC.TypeString, # (deprecated)
                PROP.CHARSET : FC.TypeCharSet,
                PROP.LANG : FC.TypeString,
                PROP.FONTVERSION : FC.TypeInteger,
                PROP.FULLNAME : FC.TypeString,
                PROP.FAMILYLANG : FC.TypeString,
                PROP.STYLELANG : FC.TypeString,
                PROP.FULLNAMELANG : FC.TypeString,
                PROP.CAPABILITY : FC.TypeString,
                PROP.FONTFORMAT : FC.TypeString,
                PROP.EMBOLDEN : FC.TypeBool,
                PROP.EMBEDDED_BITMAP : FC.TypeBool,
                PROP.DECORATIVE : FC.TypeBool,
                PROP.LCD_FILTER : FC.TypeInteger,
                PROP.FONT_FEATURES : FC.TypeString,
                PROP.NAMELANG : FC.TypeString,
                PROP.PRGNAME : FC.TypeString,
                PROP.HASH : FC.TypeString,
                PROP.POSTSCRIPT_NAME : FC.TypeString,
            }[self]
    #end fc_type

#end PROP
PROP.prop = dict((p.value, p) for p in PROP)

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
fc.FcConfigGetSysRoot.restype = ct.c_void_p
fc.FcConfigGetSysRoot.argtypes = (ct.c_void_p,)
fc.FcConfigSetSysRoot.restype = None
fc.FcConfigSetSysRoot.argtypes = (ct.c_void_p, ct.c_void_p)

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

# TODO: atomic

fc.FcFontSetMatch.restype = ct.c_void_p
fc.FcFontSetMatch.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_void_p, ct.c_void_p)
fc.FcFontMatch.restype = ct.c_void_p
fc.FcFontMatch.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
fc.FcFontRenderPrepare.restype = ct.c_void_p
fc.FcFontRenderPrepare.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
fc.FcFontSetSort.restype = ct.c_void_p
fc.FcFontSetSort = (ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_void_p, FC.Bool, ct.c_void_p, ct.c_void_p)
fc.FcFontSort.restype = ct.c_void_p
fc.FcFontSort.argtypes = (ct.c_void_p, ct.c_void_p, FC.Bool, ct.c_void_p, ct.c_void_p)
# FcFontSetSortDestroy deprecated, use FcFontSetDestroy instead

# probably don’t need rest of matrix stuff
fc.FcMatrixCopy.restype = ct.c_void_p
fc.FcMatrixCopy.argtypes = (ct.c_void_p,)

# TODO: name

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
# cannot correctly use calls that take FC.Value args (see note on class definition above for why)
#fc.FcValueDestroy.restype = None
#fc.FcValueDestroy.argtypes = (FC.Value,)
#fc.FcValueSave.restype = FC.Value
#fc.FcValueSave.argtypes = (FC.Value,)
fc.FcPatternDestroy.restype = None
fc.FcPatternDestroy.argtypes = (ct.c_void_p,)
fc.FcPatternFilter.restype = ct.c_void_p
fc.FcPatternFilter.argtypes = (ct.c_void_p, ct.c_void_p)
fc.FcPatternEqual.restype = FC.Bool
fc.FcPatternEqual.argtypes = (ct.c_void_p, ct.c_void_p)
fc.FcPatternEqualSubset.restype = FC.Bool
fc.FcPatternEqualSubset.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
fc.FcPatternHash.restype = ct.c_uint
fc.FcPatternHash.argtypes = (ct.c_void_p,)
#fc.FcPatternAdd.restype = FC.Bool
#fc.FcPatternAdd.argtypes = (ct.c_void_p, ct.c_char_p, FC.Value, FC.Bool)
#fc.FcPatternAddWeak.restype = FC.Bool
#fc.FcPatternAddWeak.argtypes = (ct.c_void_p, ct.c_char_p, FC.Value, FC.Bool)
fc.FcPatternGet.restype = ct.c_uint
fc.FcPatternGet.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int, ct.POINTER(FC.Value))
fc.FcPatternDel.restype = FC.Bool
fc.FcPatternDel.argtypes = (ct.c_void_p, ct.c_char_p)
fc.FcPatternRemove.restype = FC.Bool
fc.FcPatternRemove.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int)
# have to use separately-typed Add/Get methods because of problems with FC.Value structs
fc.FcPatternAddInteger.restype = FC.Bool
fc.FcPatternAddInteger.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int)
fc.FcPatternAddDouble.restype = FC.Bool
fc.FcPatternAddDouble.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_double)
fc.FcPatternAddString.restype = FC.Bool
fc.FcPatternAddString.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_char_p)
fc.FcPatternAddMatrix.restype = FC.Bool
fc.FcPatternAddMatrix.argtypes = (ct.c_void_p, ct.c_char_p, ct.POINTER(FC.Matrix))
fc.FcPatternAddCharSet.restype = FC.Bool
fc.FcPatternAddCharSet.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_void_p)
fc.FcPatternAddBool.restype = FC.Bool
fc.FcPatternAddBool.argtypes = (ct.c_void_p, ct.c_char_p, FC.Bool)
fc.FcPatternAddLangSet.restype = FC.Bool
fc.FcPatternAddLangSet.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_void_p)
fc.FcPatternGetInteger.restype = ct.c_uint
fc.FcPatternGetInteger.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int, ct.POINTER(ct.c_int))
fc.FcPatternGetDouble.restype = ct.c_uint
fc.FcPatternGetDouble.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int, ct.POINTER(ct.c_double))
fc.FcPatternGetString.restype = ct.c_uint
fc.FcPatternGetString.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int, ct.POINTER(ct.c_void_p))
fc.FcPatternGetMatrix.restype = ct.c_uint
fc.FcPatternGetMatrix.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int, ct.POINTER(FC.Matrix))
fc.FcPatternGetCharSet.restype = ct.c_uint
fc.FcPatternGetCharSet.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int, ct.POINTER(ct.c_void_p))
fc.FcPatternGetBool.restype = ct.c_uint
fc.FcPatternGetBool.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int, ct.POINTER(FC.Bool))
fc.FcPatternGetLangSet.restype = ct.c_uint
fc.FcPatternGetLangSet.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int, ct.POINTER(ct.c_void_p))
# not bothering with Build methods
fc.FcPatternFormat.restype = ct.c_void_p
fc.FcPatternFormat.argtypes = (ct.c_void_p, ct.c_char_p)

fc.FcStrCopy.restype = ct.c_char_p
fc.FcStrCopy.argtypes = (ct.c_void_p,)
fc.FcStrFree.restype = None
fc.FcStrFree.argtypes = (ct.c_void_p,)
# probably don’t need rest of str/utf stuff

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

fc.FcConfigParseAndLoad.restype = FC.Bool
fc.FcConfigParseAndLoad.argtypes = (ct.c_void_p, ct.c_char_p, FC.Bool)

# from fcfreetype.h

fc.FcPatternGetFTFace.restype = ct.c_uint
fc.FcPatternGetFTFace.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int, ct.POINTER(ct.c_void_p))
fc.FcPatternAddFTFace.restype = FC.Bool
fc.FcPatternAddFTFace.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_void_p)
fc.FcFreeTypeQueryFace.restype = ct.c_void_p
fc.FcFreeTypeQueryFace.argtypes = (ct.c_void_p, ct.c_char_p, ct.c_int, ct.c_void_p)

# other

libc.free.argtypes = (ct.c_void_p,)

class CallFailed(Exception) :
    "used internally for reporting general failure from calling a Fontconfig routine."

    __slots__ = ("funcname",)

    def __init__(self, funcname) :
        self.args = ("%s failed" % funcname,)
        self.funcname = funcname
    #end __init__

#end CallFailed

def init() :
    if fc.FcInit() == 0 :
        raise CallFailed("FcInit")
    #end if
#end init

def reinitialize() :
    if fc.FcInitReinitialize() == 0 :
        raise CallFailed("FcInitReinitialize")
    #end if
#end reinitialize

def init_bring_uptodate() :
    if fc.FcInitBringUptoDate() == 0 :
        raise CallFailed("FcInitBringUptoDate")
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
        raise CallFailed("FcLangNormalize")
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
            "_created",
        )

    def __init__(self, _fcobj, _created) :
        self._fcobj = _fcobj
        self._created = _created
    #end __init__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            if self._created :
                fc.FcLangSetDestroy(self._fcobj)
            #end if
            self._fcobj = None
        #end if
    #end __del__

    @classmethod
    def create(celf) :
        return \
            celf(fc.FcLangSetCreate(), True)
    #end create

    def copy(self) :
        return \
            celf(fc.FcLangSetCopy(self._fcobj), True)
    #end copy

    def add(self, lang) :
        if fc.FcLangSetAdd(self._fcobj, lang.encode()) == 0 :
            raise CallFailed("FcLangSetAdd")
        #end if
    #end add

    def remove(self, lang) :
        if fc.FcLangSetDel(self._fcobj, lang.encode()) == 0 :
            raise CallFailed("FcLangSetDel")
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
        if other != None :
            if not isinstance(other, LangSet) :
                raise TypeError("other must also be a LangSet")
            #end if
            result = fc.FcLangSetEqual(self._fcobj, other._fcobj) != 0
        else :
            result = False
        #end if
        return \
            result
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
            if isinstance(s, PROP) :
                s = s.value
            #end if
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
    "wrapper for FcBlanks objects, which represent a set of character codes which" \
    " are expected to be blank. These are used, for example, when scanning fonts," \
    " to distinguish blank characters from unmapped ones.\n" \
    "\n" \
    "Do not instantiate directly: use the create method.\n" \
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
            raise CallFailed("FcBlanksAdd")
        #end if
    #end add

    def __contains__(self, elt) :
        return \
            fc.FcBlanksIsMember(self._fcobj, elt) != 0
    #end __contains__

#end Blanks

class Config :
    "high-level wrapper around FcConfig objects. Do not instantiate directly;" \
    " use the create or get_current methods."

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
            raise CallFailed("FcConfigSetCurrent")
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
            raise CallFailed("FcConfigBuildFonts")
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
            Blanks(fc.FcConfigGetBlanks(self._fcobj), False)
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
            raise CallFailed("FcConfigSetRescanInterval")
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
            raise CallFailed("FcConfigAppFontAddFile")
        #end if
    #end app_font_add_file

    def app_font_add_dir(self, dirname) :
        if fc.FcConfigAppFontAddDir(self._fcobj, dirname.encode()) == 0 :
            raise CallFailed("FcConfigAppFontAddDir")
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
            raise CallFailed("FcConfigSubstituteWithPat")
        #end if
    #end substitute_with_pat

    def substitute(self, p, kind) :
        "kind must be FC.FcMatchPattern, FC.FcMatchFont or FC.FcMatchScan."
        if not isinstance(p, Pattern) :
            raise TypeError("second arg must be Pattern")
        #end if
        if fc.FcConfigSubstitute(self._fcobj, p._fcobj, kind) == 0 :
            raise CallFailed("FcConfigSubstitute")
        #end if
    #end substitute

    @property
    def sysroot(self) :
        result = fc.FcConfigGetSysRoot(self._fcobj)
        if result != None :
            result = ct.cast(result, ct.c_char_p).value.decode()
        else :
            result = None
        #end if
        return \
            result
    #end sysroot

    @sysroot.setter
    def sysroot(self, newroot) :
        # note: trying to pass NULL second arg to FcConfigSetSysRoot will segfault!
        fc.FcConfigSetSysRoot(self._fcobj, newroot.encode())
    #end sysroot

    def font_set_list(self, sets, pat, props) :
        if not isinstance(pat, Pattern) :
            raise TypeError("pat must be a Pattern")
        #end if
        nr_sets, f_sets, c_sets = FontSet.to_fc_list(sets)
        os = ObjectSet.to_fc(props)
        result = fc.FcFontSetList \
          (
            self._fcobj,
            ct.cast(c_sets, ct.c_void_p),
            nr_sets,
            pat._fcobj,
            os._fcobj
          )
        return \
            FontSet(result, True).from_fc()
    #end font_set_list

    def font_list(self, pat, props) :
        "finds all fonts matching Pattern pat, and returns a tuple of" \
        " Patterns describing them, containing only the properties named" \
        " in props."
        if not isinstance(pat, Pattern) :
            raise TypeError("pat must be a Pattern")
        #end if
        if props != None :
            os = ObjectSet.to_fc(props)
            c_props = os._fcobj
        else :
            c_props = None
        #end if
        # first arg to FcFontList can also be null, but I never take advantage of that
        result = fc.FcFontList(self._fcobj, pat._fcobj, c_props)
        return \
            FontSet(result, True).from_fc()
    #end font_list

    def font_set_match(self, sets, pat) :
        if not isinstance(pat, Pattern) :
            raise TypeError("pat must be a Pattern")
        #end if
        nr_sets, f_sets, c_sets = FontSet.to_fc_list(sets)
        result_status = ct.c_uint()
        result_pat = fc.FcFontSetMatch \
          (
            self._fcobj,
            ct.cast(c_sets, ct.c_void_p),
            nr_sets,
            pat._fcobj,
            ct.byref(result_status)
          )
        return \
            (Pattern(result_pat), result_status.value)
    #end font_set_match

    def font_match(self, pat) :
        if not isinstance(pat, Pattern) :
            raise TypeError("pat must be a Pattern")
        #end if
        result_status = ct.c_uint()
        result_pat = fc.FcFontMatch(self._fcobj, pat._fcobj, ct.byref(result_status))
        return \
            (Pattern(result_pat), result_status.value)
    #end font_match

    def font_render_prepare(self, pat, font) :
        if not isinstance(pat, Pattern) or not isinstance(font, Pattern) :
            raise TypeError("pat and font must be Patterns")
        #end if
        result = fc.FcFontRenderPrepare(self._fcobj, pat._fcobj, font._fcobj)
        return \
            Pattern(result)
    #end font_render_prepare

    def font_set_sort(self, sets, pat, trim, want_coverage) :
        if not isinstance(pat, Pattern) :
            raise TypeError("pat must be a Pattern")
        #end if
        nr_sets, f_sets, c_sets = FontSet.to_fc_list(sets)
        if want_coverage :
            c_coverage = ct.c_void_p()
            coverage_arg = ct.byref(c_coverage)
        else :
            c_coverage = None
            coverage_arg = None
        #end if
        result_status = ct.c_uint()
        result_set = fc.FcFontSetSort \
          (
            self._fcobj,
            ct.cast(c_sets, ct.c_void_p),
            nr_sets,
            pat._fcobj,
            FC.Bool(trim),
            coverage_arg,
            ct.byref(result_status)
          )
        if want_coverage :
            coverage = CharSet(c_coverage.value, True)
        #end if
        return \
            (
                FontSet(result_set, True).from_fc(),
                (lambda : None, lambda : coverage.from_fc())[want_coverage](),
                result_status.value
            )
    #end font_set_sort

    def font_sort(self, pat, trim, want_coverage) :
        if not isinstance(pat, Pattern) :
            raise TypeError("pat must be a Pattern")
        #end if
        if want_coverage :
            c_coverage = ct.c_void_p()
            coverage_arg = ct.byref(c_coverage)
        else :
            c_coverage = None
            coverage_arg = None
        #end if
        result_status = ct.c_uint()
        result_set = fc.FcFontSort \
          (
            self._fcobj,
            pat._fcobj,
            FC.Bool(trim),
            coverage_arg,
            ct.byref(result_status)
          )
        if want_coverage :
            coverage = CharSet(c_coverage.value, True)
        #end if
        return \
            (
                FontSet(result_set, True).from_fc(),
                (lambda : None, lambda : coverage.from_fc())[want_coverage](),
                result_status.value
            )
    #end font_sort

    def parse_and_load(self, filename, complain) :
        if fc.FcConfigParseAndLoad(self._fcobj, filename.encode(), FC.Bool(complain)) == 0 :
            raise CallFailed("FcConfigParseAndLoad")
        #end if
    #end parse_and_load

#end Config

class CharSet :
    "wrapper around FcCharSet objects. For internal use only: all relevant" \
    " functions will pass and return Python sequences."

    __slots__ = \
        ( # to forestall typos
            "_fcobj",
            "_created",
        )

    def __init__(self, _fcobj, _created) :
        if isinstance(_fcobj, ct.c_void_p) :
            _fcobj = _fcobj.value
        #end if
        self._fcobj = _fcobj
        self._created = _created
    #end __init__

    def __del__(self) :
        if fc != None and self._fcobj != None :
            if self._created :
                fc.FcCharSetDestroy(self._fcobj)
            #end if
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
            celf(result, True)
    #end to_fc

    def from_fc(self) :
        result = set()
        page = FC.charset_page()
        retrieve = fc.FcCharSetFirstPage
        next = FC.Char32(0)
        while True :
            prev = next.value
            base = retrieve(self._fcobj, ct.byref(page), ct.byref(next))
            if base == FC.CHARSET_DONE :
                break
            if next.value == prev :
                # happens intermittently!?
                #raise AssertionError("CharSet page empty at base = %08x, page = %08x\n" % (base, next.value))
                break
            #end if
            for i in range(len(page)) :
                for j in range(32) :
                    if 1 << j & page[i] != 0 :
                        result.add(base + i * 32 + j)
                        got_one = True
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
        raise CallFailed("FcStrCopyFilename")
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
                raise CallFailed("FcFontSetAdd")
            #end if
        #end for
        return \
            result
    #end to_fc

    @classmethod
    def to_fc_list(celf, sets) :
        nr_sets = len(sets)
        f_sets = tuple(FontSet.to_fc(s) for s in sets)
          # caller will need to keep these around to ensure the FcFontSet
          # objects don’t disappear
        c_sets = (ct.c_void_p * nr_sets)()
        for i in range(nr_sets) :
            c_sets[i] = f_sets[i]._fcobj
        #end for
        return \
            (nr_sets, f_sets, c_sets)
    #end to_fc_list

    def each(self) :
        f = ct.cast(self._fcobj, ct.POINTER(FC.FontSet))
        pats = ct.cast(f[0].fonts, ct.POINTER(ct.c_void_p))
        for i in range(f[0].nfont) :
            fc.FcPatternReference(pats[i])
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

    def __init__(self, *, xx, xy, yx, yy) :
        self.xx = xx
        self.xy = xy
        self.yx = yx
        self.yy = yy
    #end __init__

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
    def create(celf, vals = None) :
        self = celf(fc.FcPatternCreate())
        if vals != None :
            self.build(vals)
        #end if
        return \
            self
    #end create

    @classmethod
    def freetype_query(celf, filename, id, blanks) :
        "constructs a Pattern representing the font with index id in the font file" \
        " with the given name. Also returns the count of fonts in the file."
        if blanks != None and not isinstance(blanks, Blanks) :
            raise TypeError("blanks must be None or a Blanks")
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

    if freetype != None :

        @classmethod
        def freetype_query_face(celf, face, filename, id, blanks) :
            "constructs a Pattern representing the given freetype2.Face. It is assumed" \
            " to have been the font with index id loaded from the specified file name;" \
            " this information is included in the pattern."
            if not isinstance(face, freetype.Face) :
                raise TypeError("face must be a freetype.Face")
            #end if
            if blanks != None and not isinstance(blanks, Blanks) :
                raise TypeError("blanks must be None or a Blanks")
            #end if
            if blanks != None :
                c_blanks = blanks._fcobj
            else :
                c_blanks = None
            #end if
            result = fc.FcFreeTypeQueryFace(face._ftobj, filename.encode(), id, c_blanks)
            return \
                celf(result)
        #end freetype_query_face

    #end if

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

    def __eq__(self, other) :
        if other != None :
            if not isinstance(other, Pattern) :
                raise TypeError("other arg is not a Pattern")
            #end if
            result = fc.FcPatternEqual(self._fcobj, other._fcobj) != 0
        else :
            result = False
        #end if
        return \
            result
    #end __eq__

    def equal_subset(self, other, props) :
        if not isinstance(other, Pattern) :
            raise TypeError("other arg is not a Pattern")
        #end if
        os = ObjectSet.to_fc(props)
        return \
            fc.FcPatternEqualSubset(self._fcobj, other._fcobj, os._fcobj) != 0
    #end equal_subset

    def hash(self) :
        return \
            fc.FcPatternHash(self._fcobj)
    #end hash
    # __hash__ = hash # should I do this?

    def add(self, name, value) :

        convs = \
            {
                int : (fc.FcPatternAddInteger, None, None, False),
                float : (fc.FcPatternAddDouble, None, None, False),
                str : (fc.FcPatternAddString, lambda s : s.encode(), None, False),
                Matrix : (fc.FcPatternAddMatrix, lambda m : m.to_fc(), lambda m : m._fcobj, True),
                set : (fc.FcPatternAddCharSet, lambda c : CharSet.to_fc(c), lambda c : c._fcobj, False),
                bool : (fc.FcPatternAddBool, lambda b : FC.Bool(b), None, False),
                LangSet : (fc.FcPatternAddLangSet, None, lambda l : l._fcobj, False),
            }
        if freetype != None :
            convs[freetype.Face] = (fc.FcPatternAddFTFace, None, lambda f : f._ftobj, False)
        #end if

    #begin add
        if isinstance(name, PROP) :
            name = name.value
        #end if
        conv_type = type(value)
        if conv_type not in convs :
            conv_types = iter(convs.keys())
            while True :
                conv_type = next(conv_types, None)
                if conv_type == None :
                    raise TypeError \
                      (
                        "cannot convert %s type to Fontconfig equivalent" % type(value).__name__
                      )
                #end if
                if isinstance(value, conv_type) :
                    break
            #end while
        #end if
        func, wrap, extr, byref = convs[conv_type]
        if wrap != None :
            value1 = wrap(value)
              # keep reference to this Python object so ctypes object does not
              # disappear prematurely
        else :
            value1 = value
        #end if
        if extr != None :
            c_value = extr(value1)
        else :
            c_value = value1
        #end if
        if byref :
            c_arg = ct.byref(c_value)
        else :
            c_arg = c_value
        #end if
        if func(self._fcobj, name.encode(), c_arg) == 0 :
            raise CallFailed("FcPatternAdd")
        #end if
    #end add

    def build(self, vals) :
        for name, val in vals :
            self.add(name, val)
        #end for
    #end build

    def get(self, name, id) :

        convs = \
            {
                FC.TypeInteger : (fc.FcPatternGetInteger, ct.c_int, None),
                FC.TypeDouble : (fc.FcPatternGetDouble, ct.c_double, None),
                FC.TypeString : (fc.FcPatternGetString, ct.c_void_p, lambda p : ct.cast(p, ct.c_char_p).value.decode()),
                FC.TypeMatrix : (fc.FcPatternGetMatrix, FC.Matrix, lambda v : Matrix.from_fc(v.m.contents)),
                FC.TypeCharSet : (fc.FcPatternGetCharSet, ct.c_void_p, lambda c : CharSet(c, False).from_fc()),
                FC.TypeBool : (fc.FcPatternGetBool, FC.Bool, lambda b : b != 0),
                FC.TypeFTFace : (fc.FcPatternGetFTFace, ct.c_void_p, lambda p : p.value), # return void pointer if python_freetype is not available
                FC.TypeLangSet : (fc.FcPatternGetLangSet, ct.c_void_p, lambda l : LangSet(l, False).langs),
            }
        if freetype != None :
            convs[FC.TypeFTFace] = \
                (fc.FcPatternGetFTFace, ct.c_void_p, lambda p : freetype.Face(None, p.value, None))
        #end if

    #begin get
        name = PROP.ensure_prop(name)
        func, c_type, extr = convs[name.fc_type]
        c_arg = c_type()
        status = func(self._fcobj, name.value.encode(), id, ct.byref(c_arg))
        if status == FC.ResultTypeMismatch :
            raise TypeError("value is not of expected type")
        #end if
        if status == FC.ResultMatch :
            if extr != None :
                result = extr(c_arg)
            else :
                result = c_arg.value
            #end if
        else :
            result = None
        #end if
        return \
            (result, status)
    #end get

    def remove_all(self, name) :
        name = PROP.ensure_str(name)
        return \
            fc.FcPatternDel(self._fcobj, name.encode()) != 0
    #end remove_all

    def remove(self, name, id) :
        name = PROP.ensure_str(name)
        return \
            fc.FcPatternRemove(self._fcobj, name.encode(), id) != 0
    #end remove

    def format(self, fmt) :
        s = fc.FcPatternFormat(self._fcobj, fmt.encode())
        result = ct.cast(s, ct.c_char_p).value.decode()
        fc.FcStrFree(s)
        return \
            result
    #end format

    @property
    def each_prop(self) :
        "iterates over each property name, index and corresponding value."
        for prop in PROP :
            id = 0
            while True :
                result, status = self.get(prop, id)
                if status != FC.ResultMatch :
                    break
                yield prop, id, result
                id += 1
            #end while
        #end for
    #end each_prop

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
            raise CallFailed("FcStrSetCreate")
        #end if
        for s in pyset :
            if fc.FcStrSetAdd(result, s) == 0 :
                raise CallFailed("FcStrSetAdd")
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
