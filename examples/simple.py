from pynary import IOobject, IOStream, cast_object, types
from dataclasses import dataclass, field
from typing import TypeAlias

@IOobject
class Blob(IOStream):
	size: types.INT_BE
	text: types.BYTES_BE

	@classmethod
	def new(cls, *, text: str) -> 'Blob':
		return cast_object(Blob, {'size': len(text), 'text': text.encode('utf8')})

	@classmethod
	def to(cls, b: 'Blob') -> str:
		return b[1] # pyright: ignore

	def read(self):
		return self.size, self.text

	def write(self, text: bytes):
		self.size = types.INT_BE(len(text))
		self.text = types.BYTES_BE(text)

@IOobject
class SBlob(IOStream):
	size: types.INT_BE
	text: types.STR_BE

	@classmethod
	def new(cls, *, text: str) -> 'SBlob':
		return cast_object(SBlob, {'size': len(text), 'text': text.encode('utf8')})

	@classmethod
	def to(cls, b: 'SBlob') -> str:
		return b[1] # pyright: ignore

	def read(self):
		return self.size, self.text

	def write(self, text: str):
		self.size = types.INT_BE(len(text))
		self.text = types.STR_BE(text.encode('utf8'))

@IOobject
class Integer(IOStream):
	N: types.INT_BE

	@classmethod
	def new(cls, n, **kwargs) -> 'Integer':
		return cast_object(Integer, {'N': n})

	def read(self):
		return self.N

	def write(self, n):
		self.N = types.INT_BE(n)

@IOobject
class Field(IOStream):
	start: types.CHAR_BE
	case: types.CHAR_BE
	space: types.CHAR_BE
	key: SBlob

	def read(self):
		start = self.start
		case = self.case
		space = self.space
		key = self.key
		return case, SBlob.to(key)

	def write(self, case: str, key):
		self.start = types.CHAR_BE(b':')
		self.case = types.CHAR_BE(case[0].encode('utf8'))
		self.space = types.CHAR_BE(b' ')
		self.key = SBlob.new(text=key)

ParamValue: TypeAlias = int | str | bytes | list[str] | None

@dataclass
class parameter:
	type: str
	key: str
	value: ParamValue

@dataclass
class structure:
	parameters: list[parameter] = field(default_factory=list)
	args: list[str] = field(default_factory=list)

	def __getitem__(self, key):
		for p in self.parameters:
			if p.key == key:
				return p
		raise IndexError

	def add_parameter(self, type: str, key: str, value: ParamValue):
		self.parameters.append(parameter(type, key, value))
		return self
		
	@classmethod
	def read(cls, io):
		self = cls()
		while True:
			f = Field(io)
			case, key = f.read()
			if case == 'i':
				self.parameters.append(parameter(str(case), key, int(Integer(io).read())))
			elif case == 'b':
				self.parameters.append(parameter(str(case), key, Blob(io).read()[1]))
			elif case == 'B':
				self.parameters.append(parameter(str(case), key, str(SBlob(io).read()[1])))
			elif case == 'l':
				nargs = Integer(io).read()
				self.parameters.append(parameter(str(case), key,
					 [str(SBlob(io).read()[1]) for i in range(nargs)]
				))
			elif case == 'E':
				break
		return self

	def write(self, io):
		for p in self.parameters:
			Field(io).write(p.type, p.key)
			if p.type == 'i':
				assert isinstance(p.value, int)
				Integer(io).write(p.value)
			if p.type == 'b':
				assert isinstance(p.value, bytes)
				Blob(io).write(p.value)
			if p.type == 'B':
				assert isinstance(p.value, str)
				SBlob(io).write(p.value)
			if p.type == 'l':
				assert isinstance(p.value, list)
				Integer(io).write(len(p.value))
				for s in p.value:
					assert isinstance(s, str)
					SBlob(io).write(s)
		Field(io).write("E", '\0')

def read(path: str):
	with open(path, 'rb') as f:
		s = structure.read(f)
		print(s['integer'])
		print(s['array'])
		print(s['bynary blob'])
		print(s['string blob'])


def save(path: str):
	with open(path, 'wb') as f:
		s = (structure()
			.add_parameter('i', 'integer', 0)
			.add_parameter('l', 'array', ["first element", "second", "and so", "forth"])
			.add_parameter('b', 'bynary blob', b'some raw data')
			.add_parameter('B', 'string blob', 'some less raw data')
		).write(f)
