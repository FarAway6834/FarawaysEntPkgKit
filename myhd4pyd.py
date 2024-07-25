pass
'''

declaration

[pydlib.xiomh]
Python.h

[deflibs.domh]
STRINGIFY(x) #x
CONCAT(a, b) a##b

[pydlibsLvA.lvdomh]
PyObj PyObject
PyErrDeclars static PyObj *ErrorObject
ExportsCyF PyMethodDefd
CyFExports(...) static struct ExportsCyF methods[] = {Lists, {NULL, NULL}};
CyFItem(types, method) {STRINGIFY(method), method, types}
CyProt(func) PyObjectPtr func(PyObject *self, PyObject *args)
staticCyFunc(func) static CyProt(func)
PydIniterDeclarHeads(libname) void CONCAT(CONCAT(init, libname), ())
IniterSrc(libname) {PyObj* m; m = Py_InitModule(STRINGIFY(libname), methods); ErrorObject = Py_BuildValue("s", "error");}
PydIniterDeclar(libname) PydIniterDeclarHeads(libname) IniterSrc(libname)

[pydlibsLvA.thmh]
PyObj* PyObjPtr
PyObjPtr *CyFunc(PyObj *self, PyObj *args)
void *pydinitf()

[pydlibs.xiomh]
includerunstdpydlib.h
domhdeflibs.h
domhlvpydlibLvA.h
typespydlibsLvA.h

[hfilegener.py]
#make includerunstdpydlibs.h
from hfilegen import 

'''
