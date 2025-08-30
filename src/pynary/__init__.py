import struct
from typing import Any, Type, NewType, TypeAlias, BinaryIO, cast
from io import BytesIO
import inspect


__all__ = [
	"SVAL", 

	"cast_object",
	"IOStream",
	"IOobject",
	"binary_length",

	"types"
]

class SVAL:
	_format: str = ''
	_last: int = 0
	_val: Any = None
	def __get__(self, obj, objtype=None):
		if self._format in ['>s', '<s', 's']:
			bytes_ = obj._io.read(struct.calcsize(self._format) * SVAL._last)
			SVAL._last = 0
			self._val = SVAL._last
			return bytes_.decode('utf8')
		elif self._format in ['>p', '<p', 'p']:
			bytes_ = obj._io.read(struct.calcsize(self._format) * SVAL._last)
			SVAL._last = 0
			self._val = SVAL._last
			return bytes_
		elif self._format in ['>c', '<c', 'c']:
			bytes_ = obj._io.read(1)
			SVAL._last = 0
			self._val = SVAL._last
			return bytes_.decode('utf8')
		else:
			bytes_ = obj._io.read(struct.calcsize(self._format))
			SVAL._last = struct.unpack(self._format, bytes_)[0]
			self._val = SVAL._last
			return SVAL._last

	def __set__(self, obj, value):
		if self._format in ['>s', '<s', 's']:
			obj._io.write(value)
		elif self._format in ['>p', '<p', 'p']:
			obj._io.write(value)
		else:
			obj._io.write(struct.pack(self._format, value))

class _CHAR_BE(SVAL):		_format = '>c'
class _BYTE_BE(SVAL):		_format = '>b'
class _BOOL_BE(SVAL):		_format = '>?'
class _SHORT_BE(SVAL):		_format = '>h'
class _USHORT_BE(SVAL):		_format = '>H'
class _INT_BE(SVAL):		_format = '>i'
class _UINT_BE(SVAL):		_format = '>I'
class _LONG_BE(SVAL):		_format = '>l'
class _ULONG_BE(SVAL):		_format = '>L'
class _LONGLONG_BE(SVAL):	_format = '>q'
class _ULONGLONG_BE(SVAL):	_format = '>Q'
class _FLOAT_BE(SVAL):		_format = '>f'
class _DOUBLE_BE(SVAL):		_format = '>d'
class _STR_BE(SVAL):		_format = '>s'
class _BYTES_BE(SVAL):		_format = '>p'

class _CHAR_LE(SVAL):		_format = '<c'
class _BYTE_LE(SVAL):		_format = '<b'
class _BOOL_LE(SVAL):		_format = '<?'
class _SHORT_LE(SVAL):		_format = '<h'
class _USHORT_LE(SVAL):		_format = '<H'
class _INT_LE(SVAL):		_format = '<i'
class _UINT_LE(SVAL):		_format = '<I'
class _LONG_LE(SVAL):		_format = '<l'
class _ULONG_LE(SVAL):		_format = '<L'
class _LONGLONG_LE(SVAL):	_format = '<q'
class _ULONGLONG_LE(SVAL):	_format = '<Q'
class _FLOAT_LE(SVAL):		_format = '<f'
class _DOUBLE_LE(SVAL):		_format = '<d'
class _STR_LE(SVAL):		_format = '<s'
class _BYTES_LE(SVAL):		_format = '>p'


class types:
	CHAR_BE      = NewType('CHAR_BE', bytes)
	BYTE_BE      = NewType('BYTE_BE', bytes)
	BOOL_BE      = NewType('BOOL_BE', bool)
	SHORT_BE     = NewType('SHORT_BE', int)
	USHORT_BE    = NewType('USHORT_BE', int)
	INT_BE       = NewType('INT_BE', int)
	UINT_BE      = NewType('UINT_BE', int)
	LONG_BE      = NewType('LONG_BE', int)
	ULONG_BE     = NewType('ULONG_BE', int)
	LONGLONG_BE  = NewType('LONGLONG_BE', int)
	ULONGLONG_BE = NewType('ULONGLONG_BE', int)
	FLOAT_BE     = NewType('FLOAT_BE', float)
	DOUBLE_BE    = NewType('DOUBLE_BE', float)
	STR_BE       = NewType('STR_BE', bytes)
	BYTES_BE     = NewType('BYTES_BE', bytes)

	CHAR_LE      = NewType('CHAR_LE', bytes)
	BYTE_LE      = NewType('BYTE_LE', bytes)
	BOOL_LE      = NewType('BOOL_LE', bool)
	SHORT_LE     = NewType('SHORT_LE', int)
	USHORT_LE    = NewType('USHORT_LE', int)
	INT_LE       = NewType('INT_LE', int)
	UINT_LE      = NewType('UINT_LE', int)
	LONG_LE      = NewType('LONG_LE', int)
	ULONG_LE     = NewType('ULONG_LE', int)
	LONGLONG_LE  = NewType('LONGLONG_LE', int)
	ULONGLONG_LE = NewType('ULONGLONG_LE', int)
	FLOAT_LE     = NewType('FLOAT_LE', float)
	DOUBLE_LE    = NewType('DOUBLE_LE', float)
	STR_LE       = NewType('STR_LE', bytes)
	BYTES_LE     = NewType('BYTES_LE', bytes)

_GETTERS = {
	types.CHAR_BE:      _CHAR_BE,
	types.BYTE_BE:      _BYTE_BE,
	types.BOOL_BE:      _BOOL_BE,
	types.SHORT_BE:     _SHORT_BE,
	types.USHORT_BE:    _USHORT_BE,
	types.INT_BE:       _INT_BE,
	types.UINT_BE:      _UINT_BE,
	types.LONG_BE:      _LONG_BE,
	types.ULONG_BE:     _ULONG_BE,
	types.LONGLONG_BE:  _LONGLONG_BE,
	types.ULONGLONG_BE: _ULONGLONG_BE,
	types.FLOAT_BE:     _FLOAT_BE,
	types.DOUBLE_BE:    _DOUBLE_BE,
	types.STR_BE:       _STR_BE,
	types.BYTES_BE:     _BYTES_BE,

	types.CHAR_LE:      _CHAR_LE,
	types.BYTE_LE:      _BYTE_LE,
	types.BOOL_LE:      _BOOL_LE,
	types.SHORT_LE:     _SHORT_LE,
	types.USHORT_LE:    _USHORT_LE,
	types.INT_LE:       _INT_LE,
	types.UINT_LE:      _UINT_LE,
	types.LONG_LE:      _LONG_LE,
	types.ULONG_LE:     _ULONG_LE,
	types.LONGLONG_LE:  _LONGLONG_LE,
	types.ULONGLONG_LE: _ULONGLONG_LE,
	types.FLOAT_LE:     _FLOAT_LE,
	types.DOUBLE_LE:    _DOUBLE_LE,
	types.STR_LE:       _STR_LE,
	types.BYTES_LE:     _BYTES_LE,
}

_SIZES = {
	types.CHAR_BE:      struct.calcsize('>c'),
	types.BYTE_BE:      struct.calcsize('>b'),
	types.BOOL_BE:      struct.calcsize('>?'),
	types.SHORT_BE:     struct.calcsize('>h'),
	types.USHORT_BE:    struct.calcsize('>H'),
	types.INT_BE:       struct.calcsize('>i'),
	types.UINT_BE:      struct.calcsize('>I'),
	types.LONG_BE:      struct.calcsize('>l'),
	types.ULONG_BE:     struct.calcsize('>L'),
	types.LONGLONG_BE:  struct.calcsize('>q'),
	types.ULONGLONG_BE: struct.calcsize('>Q'),
	types.FLOAT_BE:     struct.calcsize('>f'),
	types.DOUBLE_BE:    struct.calcsize('>d'),
	types.STR_BE:       0,  # Variable size
	types.BYTES_BE:     0,  # Variable size

	types.CHAR_LE:      struct.calcsize('<c'),
	types.BYTE_LE:      struct.calcsize('<b'),
	types.BOOL_LE:      struct.calcsize('<?'),
	types.SHORT_LE:     struct.calcsize('<h'),
	types.USHORT_LE:    struct.calcsize('<H'),
	types.INT_LE:       struct.calcsize('<i'),
	types.UINT_LE:      struct.calcsize('<I'),
	types.LONG_LE:      struct.calcsize('<l'),
	types.ULONG_LE:     struct.calcsize('<L'),
	types.LONGLONG_LE:  struct.calcsize('<q'),
	types.ULONGLONG_LE: struct.calcsize('<Q'),
	types.FLOAT_LE:     struct.calcsize('<f'),
	types.DOUBLE_LE:    struct.calcsize('<d'),
	types.STR_LE:       0,  # Variable size
	types.BYTES_LE:     0,  # Variable size
}


def cast_object[T](type_: Type[T], values) -> T:
	if isinstance(values, (list, list)):
		for e in values:
			if not isinstance(e, (tuple, list)):
				raise TypeError("values must be a dict of property and values or a list that can be casted to such a dict")
		values = dict(values)
	if not isinstance(values, dict):
		raise TypeError("values must be a dict of property and values or a list that can be casted to such a dict")
	return cast(T, values)


class IOStream:
	def __init__(self, _io: BinaryIO):
		self._io = _io
		annotations = inspect.get_annotations(type(self))
		for k, t in annotations.items():
			if isinstance(t, type) and issubclass(t, IOStream):
				setattr(self, k, t(self._io))


class _descr:
	def __init__(self, _type):
		self._type = _type
		self._instance = None

	def __get__(self, obj, objtype=None):
		return [getattr(self._instance, i) for i in self._type._getters]

	def __set__(self, obj, values):
		if isinstance(values, self._type):
			self._instance = values
			return 
		for k in self._type._getters:
			setattr(self._instance, k, values[k])


def IOobject(c):
	annotations = inspect.get_annotations(c)
	c._is_ioobject = True
	c._getters = []
	binary_size = 0
	
	for k, t in annotations.items():
		if t in _GETTERS:
			setattr(c, k, _GETTERS[t]())
			c._getters.append(k)
			binary_size += _SIZES[t]
		if hasattr(t, '_is_ioobject') and t._is_ioobject:
			setattr(c, k, _descr(t))
			assert hasattr(t, "__binary_length__")
			binary_size += t.__binary_length__
	
	c.__binary_length__ = binary_size

	def __get__(self, obj, objtype=None):
		for i in self._getters:
			yield getattr(self, i)

	def __set__(self, obj, values):
		for k in self._getters:
			setattr(self, k, values[k])

	c.__get__ = __get__
	c.__set__ = __set__
	return c


def binary_length(obj_class) -> int:
	if not hasattr(obj_class, '__binary_length__'):
		raise ValueError(f"Object {obj_class} is not decorated with @IOobject")
	return obj_class.__binary_length__
