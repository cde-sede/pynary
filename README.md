# pynary


A library used to define how objects can be read or written inside a byte stream.

### Example

```python
from pynary import IOobject, IOStream, types
from io import BytesIO

@IOobject
class Example(IOStream):
    a: types.INT_BE # INTEGER BIG ENDIAN
    b: types.SHORT_BE # SHORT BIG ENDIAN

    def read(self):
        return self.a, self.b

b = BytesIO()
Example(b).write(1, 2)
b.seek(0)
print(b.read())
b.seek(0)
print(Example(b).read())
```


More complex behavior can be done by nesting classes

See [this](https://github.com/cde-sede/pynary/blob/main/examples/simple.py) for a concrete example.
