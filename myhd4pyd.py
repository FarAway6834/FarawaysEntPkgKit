pass
'''

declaration

Python.h

PyObj PyObject
PyErrDeclars static PyObj *ErrorObject
ExportsCyF PyMethodDefd
CyFExports(...) static struct ExportsCyF methods[] = {__VA_ARGS__, {NULL, NULL}};
STRINGIFY(x) #x
CyFItem(types, method) {STRINGIFY(method), method, types}

PyObj* PyObjPtr
PyObjPtr *CyFunc(PyObj *self, PyObj *args)

CyProt(func) PyObjectPtr func(PyObject *self, PyObject *args)
staticCyFunc(func) static CyProt(func)

'''
