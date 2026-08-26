"""
Karakoram panorama — peak dataset.

Imported by views.py (`from .karakoram_view import PEAKS as KARAKORAM_PEAKS`)
and passed into trek_list()'s context, which trek_list.html loops over to
render the hero on the homepage. There's no standalone view here anymore --
the panorama used to live on its own page at /karakoram/, but that page and
its route were removed once the hero got embedded directly into
trek_list.html; this file kept only the data both versions shared.

The 16 peaks below are read from the supplied "Karakoram Peakscapes"
artwork; elevations are given in both metres (as printed on the artwork)
and feet (computed, 1 m = 3.280839895 ft) so the template does no math.

A couple of the smaller, greyed-out summits on the source artwork
(Marble Peak, Durbin Kangri I) print elevation figures too small to
read with full confidence even at full resolution — those two are
best-available estimates and are worth checking against the original
artwork file if exact precision matters to you. Every other figure
was cross-checked against its real-world elevation.
"""

PEAKS = [
    {"name": "Angel", "slug": "angel", "m": 6858, "m_fmt": "6,858", "ft": 22500, "ft_fmt": "22,500", "tier": "mid", "x": 6, "y": 80.56, "lift": 1},
    {"name": "Marble Peak", "slug": "marble-peak", "m": 6700, "m_fmt": "6,700", "ft": 21982, "ft_fmt": "21,982", "tier": "faint", "x": 9, "y": 86.11, "lift": 1},
    {"name": "Mitre", "slug": "mitre", "m": 6025, "m_fmt": "6,025", "ft": 19767, "ft_fmt": "19,767", "tier": "mid", "x": 13.5, "y": 83.33, "lift": 1},
    {"name": "Skyang Kangri West", "slug": "skyang-kangri-west", "m": 6721, "m_fmt": "6,721", "ft": 22051, "ft_fmt": "22,051", "tier": "faint", "x": 18.5, "y": 75.0, "lift": 2},
    {"name": "K2", "slug": "k2", "m": 8611, "m_fmt": "8,611", "ft": 28251, "ft_fmt": "28,251", "tier": "major", "x": 26, "y": 63.89, "lift": 3},
    {"name": "Broad Peak North", "slug": "broad-peak-north", "m": 7490, "m_fmt": "7,490", "ft": 24573, "ft_fmt": "24,573", "tier": "mid", "x": 33, "y": 76.39, "lift": 2},
    {"name": "Broad Peak", "slug": "broad-peak", "m": 8051, "m_fmt": "8,051", "ft": 26414, "ft_fmt": "26,414", "tier": "major", "x": 38.5, "y": 65.28, "lift": 3},
    {"name": "Broad Peak South", "slug": "broad-peak-south", "m": 7285, "m_fmt": "7,285", "ft": 23901, "ft_fmt": "23,901", "tier": "mid", "x": 44, "y": 75.0, "lift": 1},
    {"name": "Durbin Kangri I", "slug": "durbin-kangri-i", "m": 6234, "m_fmt": "6,234", "ft": 20453, "ft_fmt": "20,453", "tier": "faint", "x": 50, "y": 80.56, "lift": 1},
    {"name": "Gasherbrum IV", "slug": "gasherbrum-iv", "m": 7932, "m_fmt": "7,932", "ft": 26024, "ft_fmt": "26,024", "tier": "mid", "x": 56, "y": 72.22, "lift": 2},
    {"name": "Gasherbrum III", "slug": "gasherbrum-iii", "m": 7952, "m_fmt": "7,952", "ft": 26089, "ft_fmt": "26,089", "tier": "mid", "x": 61, "y": 69.44, "lift": 2},
    {"name": "Gasherbrum II", "slug": "gasherbrum-ii", "m": 8034, "m_fmt": "8,034", "ft": 26358, "ft_fmt": "26,358", "tier": "major", "x": 66.5, "y": 62.5, "lift": 3},
    {"name": "Gasherbrum V", "slug": "gasherbrum-v", "m": 7147, "m_fmt": "7,147", "ft": 23448, "ft_fmt": "23,448", "tier": "mid", "x": 72, "y": 76.39, "lift": 1},
    {"name": "Gasherbrum VI", "slug": "gasherbrum-vi", "m": 6979, "m_fmt": "6,979", "ft": 22897, "ft_fmt": "22,897", "tier": "mid", "x": 77.5, "y": 79.17, "lift": 1},
    {"name": "Gasherbrum I", "slug": "gasherbrum-i", "m": 8080, "m_fmt": "8,080", "ft": 26509, "ft_fmt": "26,509", "tier": "major", "x": 84, "y": 63.89, "lift": 3},
    {"name": "Gasherbrum I South", "slug": "gasherbrum-i-south", "m": 6404, "m_fmt": "6,404", "ft": 21010, "ft_fmt": "21,010", "tier": "mid", "x": 90.5, "y": 73.61, "lift": 1},
]