import angr

from angr.sim_type import *
from cle.backends.externs import ExternObject
from nativedroid.analyses.resolver.annotation import *
from nativedroid.analyses.resolver.jni.java_type import *
from nativedroid.analyses.resolver.jni.jni_helper import *

nativedroid_logger = logging.getLogger('nativedroid.jni_native_interface')

# Record the mapping info of dynamic register methods
DYNAMIC_REGISTER_METHODS = {}
jni_native_interface_origin_usage = {
    'GetVersion': 0,
    'DefineClass': 0,
    'FindClass': 0,
    'FromReflectedMethod': 0,
    'FromReflectedField': 0,
    'ToReflectedMethod': 0,
    'GetSuperClass': 0,
    'IsAssignableFrom': 0,
    'ToReflectedField': 0,
    'Throw': 0,
    'ThrowNew': 0,
    'ExceptionOccurred': 0,
    'ExceptionDescribe': 0,
    'ExceptionClear': 0,
    'FatalError': 0,
    'PushLocalFrame': 0,
    'PopLocalFrame': 0,
    'NewGlobalRef': 0,
    'DeleteGlobalRef': 0,
    'DeleteLocalRef': 0,
    'IsSameObject': 0,
    'NewLocalRef': 0,
    'EnsureLocalCapacity': 0,
    'AllocObject': 0,
    'NewObject': 0,
    'NewObjectV': 0,
    'NewObjectA': 0,
    'GetObjectClass': 0,
    'IsInstanceOf': 0,
    'GetMethodID': 0,
    'CallObjectMethod': 0,
    'CallObjectMethodV': 0,
    'CallObjectMethodA': 0,
    'CallBooleanMethod': 0,
    'CallBooleanMethodV': 0,
    'CallBooleanMethodA': 0,
    'CallByteMethod': 0,
    'CallByteMethodV': 0,
    'CallByteMethodA': 0,
    'CallCharMethod': 0,
    'CallCharMethodV': 0,
    'CallCharMethodA': 0,
    'CallShortMethod': 0,
    'CallShortMethodV': 0,
    'CallShortMethodA': 0,
    'CallIntMethod': 0,
    'CallIntMethodV': 0,
    'CallIntMethodA': 0,
    'CallLongMethod': 0,
    'CallLongMethodV': 0,
    'CallLongMethodA': 0,
    'CallFloatMethod': 0,
    'CallFloatMethodV': 0,
    'CallFloatMethodA': 0,
    'CallDoubleMethod': 0,
    'CallDoubleMethodV': 0,
    'CallDoubleMethodA': 0,
    'CallVoidMethod': 0,
    'CallVoidMethodV': 0,
    'CallVoidMethodA': 0,
    'CallNonvirtualObjectMethod': 0,
    'CallNonvirtualObjectMethodV': 0,
    'CallNonvirtualObjectMethodA': 0,
    'CallNonvirtualBooleanMethod': 0,
    'CallNonvirtualBooleanMethodV': 0,
    'CallNonvirtualBooleanMethodA': 0,
    'CallNonvirtualByteMethod': 0,
    'CallNonvirtualByteMethodV': 0,
    'CallNonvirtualByteMethodA': 0,
    'CallNonvirtualCharMethod': 0,
    'CallNonvirtualCharMethodV': 0,
    'CallNonvirtualCharMethodA': 0,
    'CallNonvirtualShortMethod': 0,
    'CallNonvirtualShortMethodV': 0,
    'CallNonvirtualShortMethodA': 0,
    'CallNonvirtualIntMethod': 0,
    'CallNonvirtualIntMethodV': 0,
    'CallNonvirtualIntMethodA': 0,
    'CallNonvirtualLongMethod': 0,
    'CallNonvirtualLongMethodV': 0,
    'CallNonvirtualLongMethodA': 0,
    'CallNonvirtualFloatMethod': 0,
    'CallNonvirtualFloatMethodV': 0,
    'CallNonvirtualFloatMethodA': 0,
    'CallNonvirtualDoubleMethod': 0,
    'CallNonvirtualDoubleMethodV': 0,
    'CallNonvirtualDoubleMethodA': 0,
    'CallNonvirtualVoidMethod': 0,
    'CallNonvirtualVoidMethodV': 0,
    'CallNonvirtualVoidMethodA': 0,
    'GetFieldID': 0,
    'GetObjectField': 0,
    'GetBooleanField': 0,
    'GetByteField': 0,
    'GetCharField': 0,
    'GetShortField': 0,
    'GetIntField': 0,
    'GetLongField': 0,
    'GetFloatField': 0,
    'GetDoubleField': 0,
    'SetObjectField': 0,
    'SetBooleanField': 0,
    'SetByteField': 0,
    'SetCharField': 0,
    'SetShortField': 0,
    'SetIntField': 0,
    'SetLongField': 0,
    'SetFloatField': 0,
    'SetDoubleField': 0,
    'GetStaticMethodID': 0,
    'CallStaticObjectMethod': 0,
    'CallStaticObjectMethodV': 0,
    'CallStaticObjectMethodA': 0,
    'CallStaticBooleanMethod': 0,
    'CallStaticBooleanMethodV': 0,
    'CallStaticBooleanMethodA': 0,
    'CallStaticByteMethod': 0,
    'CallStaticByteMethodV': 0,
    'CallStaticByteMethodA': 0,
    'CallStaticCharMethod': 0,
    'CallStaticCharMethodV': 0,
    'CallStaticCharMethodA': 0,
    'CallStaticShortMethod': 0,
    'CallStaticShortMethodV': 0,
    'CallStaticShortMethodA': 0,
    'CallStaticIntMethod': 0,
    'CallStaticIntMethodV': 0,
    'CallStaticIntMethodA': 0,
    'CallStaticLongMethod': 0,
    'CallStaticLongMethodV': 0,
    'CallStaticLongMethodA': 0,
    'CallStaticFloatMethod': 0,
    'CallStaticFloatMethodV': 0,
    'CallStaticFloatMethodA': 0,
    'CallStaticDoubleMethod': 0,
    'CallStaticDoubleMethodV': 0,
    'CallStaticDoubleMethodA': 0,
    'CallStaticVoidMethod': 0,
    'CallStaticVoidMethodV': 0,
    'CallStaticVoidMethodA': 0,
    'GetStaticFieldID': 0,
    'GetStaticObjectField': 0,
    'GetStaticBooleanField': 0,
    'GetStaticByteField': 0,
    'GetStaticCharField': 0,
    'GetStaticShortField': 0,
    'GetStaticIntField': 0,
    'GetStaticLongField': 0,
    'GetStaticFloatField': 0,
    'GetStaticDoubleField': 0,
    'SetStaticObjectField': 0,
    'SetStaticBooleanField': 0,
    'SetStaticByteField': 0,
    'SetStaticCharField': 0,
    'SetStaticShortField': 0,
    'SetStaticIntField': 0,
    'SetStaticLongField': 0,
    'SetStaticFloatField': 0,
    'SetStaticDoubleField': 0,
    'NewString': 0,
    'GetStringLength': 0,
    'GetStringChars': 0,
    'ReleaseStringChars': 0,
    'NewStringUTF': 0,
    'GetStringUTFLength': 0,
    'GetStringUTFChars': 0,
    'ReleaseStringUTFChars': 0,
    'GetArrayLength': 0,
    'NewObjectArray': 0,
    'GetObjectArrayElement': 0,
    'SetObjectArrayElement': 0,
    'NewBooleanArray': 0,
    'NewByteArray': 0,
    'NewCharArray': 0,
    'NewShortArray': 0,
    'NewIntArray': 0,
    'NewLongArray': 0,
    'NewFloatArray': 0,
    'NewDoubleArray': 0,
    'GetBooleanArrayElements': 0,
    'GetByteArrayElements': 0,
    'GetCharArrayElements': 0,
    'GetShortArrayElements': 0,
    'GetIntArrayElements': 0,
    'GetLongArrayElements': 0,
    'GetFloatArrayElements': 0,
    'GetDoubleArrayElements': 0,
    'ReleaseBooleanArrayElements': 0,
    'ReleaseByteArrayElements': 0,
    'ReleaseCharArrayElements': 0,
    'ReleaseShortArrayElements': 0,
    'ReleaseIntArrayElements': 0,
    'ReleaseLongArrayElements': 0,
    'ReleaseFloatArrayElements': 0,
    'ReleaseDoubleArrayElements': 0,
    'GetBooleanArrayRegion': 0,
    'GetByteArrayRegion': 0,
    'GetCharArrayRegion': 0,
    'GetShortArrayRegion': 0,
    'GetIntArrayRegion': 0,
    'GetLongArrayRegion': 0,
    'GetFloatArrayRegion': 0,
    'GetDoubleArrayRegion': 0,
    'SetBooleanArrayRegion': 0,
    'SetByteArrayRegion': 0,
    'SetCharArrayRegion': 0,
    'SetShortArrayRegion': 0,
    'SetIntArrayRegion': 0,
    'SetLongArrayRegion': 0,
    'SetFloatArrayRegion': 0,
    'SetDoubleArrayRegion': 0,
    'RegisterNatives': 0,
    'UnregisterNatives': 0,
    'MonitorEnter': 0,
    'MonitorExit': 0,
    'GetJavaVM': 0,
    'GetStringRegion': 0,
    'GetStringUTFRegion': 0,
    'GetPrimitiveArrayCritical': 0,
    'ReleasePrimitiveArrayCritical': 0,
    'GetStringCritical': 0,
    'ReleaseStringCritical': 0,
    'NewWeakGlobalRef': 0,
    'DeleteWeakGlobalRef': 0,
    'ExceptionCheck': 0,
    'NewDirectByteBuffer': 0,
    'GetDirectBufferAddress': 0,
    'GetDirectBufferCapacity': 0,
    'GetObjectRefType': 0
}

java_sas_file = ''


def get_method_taint_attribute(method_full_signature):
    """
    From TaintSourcesAndSinks.txt file get the attribute of the method
    :param str method_full_signature:
    :return:
    """
    if method_full_signature:
        for line in open(java_sas_file, 'r'):
            res = re.split(r'[ \n]', line)
            if method_full_signature == res[0]:
                if '_SOURCE_' in res:
                    return [['_SOURCE_', '_API_'], res[1]]
                elif '_SINK_' in res:
                    if len(res) == 4:
                        return ['_SINK_', 'ALL']
                    elif len(res) == 5:
                        return ['_SINK_', res[-2]]
    else:
        return None


def icc_handle(class_name, method_name, return_annotation, simproc):
    """

    :param class_name:
    :param method_name:
    :param return_annotation:
    :param simproc: Reflection call SimProcedure
    :return return_annotation
    """

    if class_name == 'android/content/Intent':
        if method_name == 'setClassName':
            for annotation in simproc.arg(4).annotations:
                if type(annotation) is JstringAnnotation:
                    return_annotation.icc_info['is_icc'] = True
                    return_annotation.icc_info['activity_name'] = annotation.value
        elif method_name == 'putExtra':
            return_annotation = simproc.arg(1).annotations[0]
            extra_key = None
            extra_value = None
            for annotation in simproc.arg(3).annotations:
                if type(annotation) is JstringAnnotation:
                    extra_key = annotation.value
            for annotation in simproc.arg(4).annotations:
                if type(annotation) is JobjectAnnotation:
                    extra_value = copy.deepcopy(annotation)
            return_annotation.icc_info['extra'] = {extra_key: extra_value}
        elif method_name == 'getStringExtra':
            for annotation in simproc.arg(3).annotations:
                if type(annotation) is JstringAnnotation:
                    return_annotation.taint_info['is_taint'] = True
                    return_annotation.taint_info['taint_type'] = ['_SOURCE_', '_API_']
                    return_annotation.taint_info['taint_info'] = ['SENSITIVE_INFO']

                    return_annotation.icc_info['is_icc'] = True
                    return_annotation.icc_info['extra'] = {annotation.value: None}
    elif class_name == 'android/content/Context':
        if method_name == 'startActivity':
            for annotation in simproc.arg(3).annotations:
                if type(annotation) is JobjectAnnotation:
                    activity_name = annotation.icc_info['activity_name']
                    extra = annotation.icc_info['extra']
                    print("Start Activity: %s, extra: %s" % (activity_name, extra))
    return return_annotation


class GetVersion(angr.SimProcedure):
    def run(self, env):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetVersion'


class DefineClass(angr.SimProcedure):
    def run(self, env, name, loader, buf, bufLen):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jclass = JClass(self.project)
        return_value = claripy.BVV(jclass.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'DefineClass'


class FindClass(angr.SimProcedure):
    def run(self, env, name):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        strlen_simproc = angr.SIM_PROCEDURES['libc']['strlen']
        name_strlen = self.inline_call(strlen_simproc, name)

        name_str = self.state.solver.eval(self.state.memory.load(name, name_strlen.ret_expr), cast_to=str)
        nativedroid_logger.info('Class: %s', name_str)

        jclass = JClass(self.project)
        return_value = claripy.BVV(jclass.ptr, self.project.arch.bits)
        return_value = return_value.annotate(JclassAnnotation(class_type=name_str, fields_info=list()))
        return return_value

    def __repr__(self):
        return 'FindClass'


class FromReflectedMethod(angr.SimProcedure):
    def run(self, env, method):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jmethod_id = JMethodID(self.project)
        return_value = claripy.BVV(jmethod_id.ptr, self.project.arch.bits)

        return return_value

    def __repr__(self):
        return 'FromReflectedMethod'


class FromReflectedField(angr.SimProcedure):
    def run(self, env, field):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jfield_id = JFieldID(self.project)
        return_value = claripy.BVV(jfield_id.ptr, self.project.arch.bits)

        return return_value

    def __repr__(self):
        return 'FromReflectedField'


class ToReflectedMethod(angr.SimProcedure):
    def run(self, env, cls, method_id, is_static):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'ToReflectedMethod'


class GetSuperClass(angr.SimProcedure):
    def run(self, env, clazz):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jclass = JClass(self.project)
        return_value = claripy.BVV(jclass.ptr, self.project.arch.bits)

        return return_value

    def __repr__(self):
        return 'GetSuperClass'


class IsAssignableFrom(angr.SimProcedure):
    def run(self, env, clazz1, clazz2):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jboolean = JBoolean(self.project)
        return_value = claripy.BVV(jboolean.ptr, self.project.arch.bits)

        return return_value

    def __repr__(self):
        return 'IsAssignableFrom'


class ToReflectedField(angr.SimProcedure):
    def run(self, env, cls, fieldID, isStatic):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)

        return return_value

    def __repr__(self):
        return 'ToReflectedField'


class Throw(angr.SimProcedure):
    def run(self, env, obj):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'Throw'


class ThrowNew(angr.SimProcedure):
    def run(self, env, clazz, message):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'ThrowNew'


class ExceptionOccurred(angr.SimProcedure):
    def run(self, env):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jthrowable = JThrowlable(self.project)
        return_value = claripy.BVV(jthrowable.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'ExceptionOccurred'


class ExceptionDescribe(angr.SimProcedure):
    def run(self, env):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ExceptionDescribe'


class ExceptionClear(angr.SimProcedure):
    def run(self, env):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ExceptionClear'


class FatalError(angr.SimProcedure):
    def run(self, env, msg):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'FatalError'


class PushLocalFrame(angr.SimProcedure):
    def run(self, env, capacity):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'PushLocalFrame'


class PopLocalFrame(angr.SimProcedure):
    def run(self, env, result):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'PopLocalFrame'


class NewGlobalRef(angr.SimProcedure):
    def run(self, env, obj):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewGlobalRef'


class DeleteGlobalRef(angr.SimProcedure):
    def run(self, env, globalRef):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'DeleteGlobalRef'


class DeleteLocalRef(angr.SimProcedure):
    def run(self, env, localRef):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'DeleteLocalRef'


class IsSameObject(angr.SimProcedure):
    def run(self, env, ref1, ref2):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jboolean = JBoolean(self.project)
        return_value = claripy.BVV(jboolean.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'IsSameObject'


class NewLocalRef(angr.SimProcedure):
    def run(self, env, ref):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewLocalRef'


class EnsureLocalCapacity(angr.SimProcedure):
    def run(self, env, capacity):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'EnsureLocalCapacity'


class AllocObject(angr.SimProcedure):
    def run(self, env, clazz):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'AllocObject'


class NewObject(angr.SimProcedure):
    def run(self, env, clazz, methodID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)

        for annotation in clazz.annotations:
            if type(annotation) is JclassAnnotation:
                return_value = return_value.annotate(
                    JobjectAnnotation(source='from_native', obj_type=annotation.class_type, fields_info=list()))

        return return_value

    def __repr__(self):
        return 'NewObject'


class NewObjectV(NewObject):
    def __repr__(self):
        return 'NewObjectV'


class NewObjectA(NewObject):
    def __repr__(self):
        return 'NewObjectA'


class GetObjectClass(angr.SimProcedure):
    def run(self, env, obj):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jclass = JClass(self.project)
        return_value = claripy.BVV(jclass.ptr, self.project.arch.bits)
        for annotation in obj.annotations:
            if type(annotation) is JobjectAnnotation:
                return_value = return_value.annotate(
                    JclassAnnotation(class_type=annotation.obj_type, fields_info=list()))

        return return_value

    def __repr__(self):
        return 'GetObjectClass'


class IsInstanceOf(angr.SimProcedure):
    def run(self, env, obj, clazz):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jboolean = JInt(self.project)
        return_value = claripy.BVV(jboolean.ptr, self.project.arch.bits)

        return return_value

    def __repr__(self):
        return 'IsInstanceOf'


class GetMethodID(angr.SimProcedure):
    def run(self, env, clazz, name, sig):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)
        strlen_simproc = angr.SIM_PROCEDURES['libc']['strlen']
        name_strlen = self.inline_call(strlen_simproc, name)
        name_str = self.state.solver.eval(self.state.memory.load(name, name_strlen.ret_expr), cast_to=str)
        signature_strlen = self.inline_call(strlen_simproc, sig)
        signature_str = self.state.solver.eval(self.state.memory.load(sig, signature_strlen.ret_expr),
                                               cast_to=str)

        jmethod_id = JMethodID(self.project)
        return_value = claripy.BVV(jmethod_id.ptr, self.project.arch.bits)

        class_name = None
        for annotation in clazz.annotations:
            if type(annotation) is JclassAnnotation:
                class_name = annotation.class_type
        nativedroid_logger.info('CLASS: %s', class_name)
        nativedroid_logger.info('METHOD: %s', name_str)
        nativedroid_logger.info('SIGN: %s', signature_str)

        return_value = return_value.annotate(
            JmethodIDAnnotation(class_name=class_name, method_name=name_str, method_signature=signature_str))

        return return_value

    def __repr__(self):
        return 'GetMethodID'


class CallObjectMethod(angr.SimProcedure):
    def run(self, env, obj, methodID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)
        num_args = 3
        for annotation in methodID.annotations:
            if type(annotation) is JmethodIDAnnotation:
                class_name = annotation.class_name
                method_name = annotation.method_name
                method_signature = annotation.method_signature
                method_full_signature = get_method_full_signature(class_name, method_name, method_signature)
                method_taint_attribute = get_method_taint_attribute(method_full_signature)
                num_args += count_arg_nums(method_signature)
                jni_return_type = get_jni_return_type(method_signature)
                java_return_type = get_java_return_type(method_signature)
                typ = get_type(self.project, java_return_type)
                typ_size = get_type_size(self.project, java_return_type)
                return_value = claripy.BVV(typ.ptr, typ_size)
                return_annotation = construct_annotation(jni_return_type, 'from_reflection_call')
                if method_taint_attribute is not None:
                    return_annotation.taint_info['is_taint'] = True
                    return_annotation.taint_info['taint_type'] = method_taint_attribute[0]
                    return_annotation.taint_info['taint_info'] = method_taint_attribute[1]
                else:
                    for anno in obj.annotations:
                        if type(anno) is JobjectAnnotation:
                            if anno.taint_info['is_taint']:
                                return_annotation.taint_info = anno.taint_info
                            else:
                                if anno.fields_info:
                                    for field_info in anno.fields_info:
                                        if field_info.is_tainted:
                                            return_annotation.taint_info = copy.deepcopy(
                                                field_info.taint_info)
                return_annotation = icc_handle(class_name, method_name, return_annotation, self)
                return_value = return_value.append_annotation(return_annotation)
                return return_value
        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'CallObjectMethod'


class CallTypeMethod(CallObjectMethod):
    def __repr__(self):
        return 'CallTypeMethod'


class CallObjectMethodV(CallTypeMethod):
    def __repr__(self):
        return 'CallObjectMethodV'


class CallObjectMethodA(CallTypeMethod):
    def __repr__(self):
        return 'CallObjectMethodA'


class CallBooleanMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallBooleanMethod'


class CallBooleanMethodV(CallTypeMethod):
    def __repr__(self):
        return 'CallBooleanMethodV'


class CallBooleanMethodA(CallTypeMethod):
    def __repr__(self):
        return 'CallBooleanMethodA'


class CallByteMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallByteMethod'


class CallByteMethodV(CallTypeMethod):
    def __repr__(self):
        return 'CallByteMethodV'


class CallByteMethodA(CallTypeMethod):
    def __repr__(self):
        return 'CallByteMethodA'


class CallCharMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallCharMethod'


class CallCharMethodV(CallTypeMethod):
    def __repr__(self):
        return 'CallCharMethodV'


class CallCharMethodA(CallTypeMethod):
    def __repr__(self):
        return 'CallCharMethodA'


class CallShortMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallShortMethod'


class CallShortMethodV(CallTypeMethod):
    def __repr__(self):
        return 'CallShortMethodV'


class CallShortMethodA(CallTypeMethod):
    def __repr__(self):
        return 'CallShortMethodA'


class CallIntMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallIntMethod'


class CallIntMethodV(CallTypeMethod):
    def __repr__(self):
        return 'CallIntMethodV'


class CallIntMethodA(CallTypeMethod):
    def __repr__(self):
        return 'CallIntMethodA'


class CallLongMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallLongMethod'


class CallLongMethodV(CallTypeMethod):
    def __repr__(self):
        return 'CallLongMethodV'


class CallLongMethodA(CallTypeMethod):
    def __repr__(self):
        return 'CallLongMethodA'


class CallFloatMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallFloatMethod'


class CallFloatMethodV(CallTypeMethod):
    def __repr__(self):
        return 'CallFloatMethodV'


class CallFloatMethodA(CallTypeMethod):
    def __repr__(self):
        return 'CallFloatMethodA'


class CallDoubleMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallDoubleMethod'


class CallDoubleMethodV(CallTypeMethod):
    def __repr__(self):
        return 'CallDoubleMethodV'


class CallDoubleMethodA(CallTypeMethod):
    def __repr__(self):
        return 'CallDoubleMethodA'


class CallVoidMethod(CallTypeMethod):
    def run(self, env, obj, methodID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        num_args = 3

        for annotation in methodID.annotations:
            if type(annotation) is JmethodIDAnnotation:
                class_name = annotation.class_name
                method_name = annotation.method_name
                method_signature = annotation.method_signature
                num_args += count_arg_nums(method_signature)
                icc_handle(class_name, method_name, None, self)

    def __repr__(self):
        return 'CallVoidMethod'


class CallVoidMethodV(CallVoidMethod):
    def __repr__(self):
        return 'CallVoidMethodV'


class CallVoidMethodA(CallVoidMethod):
    def __repr__(self):
        return 'CallVoidMethodA'


class CallNonvirtualTypeMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallNonvirtual<Type>Method'


class CallNonvirtualObjectMethod(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualObjectMethod'


class CallNonvirtualObjectMethodV(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualObjectMethodV'


class CallNonvirtualObjectMethodA(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualObjectMethodA'


class CallNonvirtualBooleanMethod(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualBooleanMethod'


class CallNonvirtualBooleanMethodV(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualBooleanMethodV'


class CallNonvirtualBooleanMethodA(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualBooleanMethodA'


class CallNonvirtualByteMethod(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualByteMethod'


class CallNonvirtualByteMethodV(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualByteMethodV'


class CallNonvirtualByteMethodA(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualByteMethodA'


class CallNonvirtualCharMethod(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualCharMethod'


class CallNonvirtualCharMethodV(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualCharMethodV'


class CallNonvirtualCharMethodA(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualCharMethodA'


class CallNonvirtualShortMethod(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualShortMethod'


class CallNonvirtualShortMethodV(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualShortMethodV'


class CallNonvirtualShortMethodA(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualShortMethodA'


class CallNonvirtualIntMethod(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualIntMethod'


class CallNonvirtualIntMethodV(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualIntMethodV'


class CallNonvirtualIntMethodA(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualIntMethodA'


class CallNonvirtualLongMethod(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualLongMethod'


class CallNonvirtualLongMethodV(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualLongMethodV'


class CallNonvirtualLongMethodA(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualLongMethodA'


class CallNonvirtualFloatMethod(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualFloatMethod'


class CallNonvirtualFloatMethodV(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualFloatMethodV'


class CallNonvirtualFloatMethodA(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualFloatMethodA'


class CallNonvirtualDoubleMethod(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualDoubleMethod'


class CallNonvirtualDoubleMethodV(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualDoubleMethodV'


class CallNonvirtualDoubleMethodA(CallNonvirtualTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualDoubleMethodA'


class CallNonvirtualVoidMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallNonvirtualVoidMethod'


class CallNonvirtualVoidMethodV(CallNonvirtualVoidMethod):
    def __repr__(self):
        return 'CallNonvirtualVoidMethodV'


class CallNonvirtualVoidMethodA(CallNonvirtualVoidMethod):
    def __repr__(self):
        return 'CallNonvirtualVoidMethodA'


class GetFieldID(angr.SimProcedure):
    def run(self, env, clazz, name, sig):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        class_name = None
        for annotation in clazz.annotations:
            if type(annotation) is JclassAnnotation:
                class_name = annotation.class_type

        strlen_simproc = angr.SIM_PROCEDURES['libc']['strlen']
        name_strlen = self.inline_call(strlen_simproc, name)
        name_str = self.state.solver.eval(self.state.memory.load(name, name_strlen.ret_expr), cast_to=str)
        signature_strlen = self.inline_call(strlen_simproc, sig)
        sig_str = self.state.solver.eval(self.state.memory.load(sig, signature_strlen.ret_expr),
                                         cast_to=str)
        nativedroid_logger.info('CLASS: %s', class_name)
        nativedroid_logger.info('FIELD: %s', name_str)
        nativedroid_logger.info('SIGN: %s', sig_str)

        jfield_id = JFieldID(self.project)
        return_value = claripy.BVV(jfield_id.ptr, self.project.arch.bits)
        return_value = return_value.annotate(
            JfieldIDAnnotation(class_name=class_name, field_name=name_str, field_signature=sig_str))

        return return_value

    def __repr__(self):
        return 'GetFieldID'


class GetObjectField(angr.SimProcedure):
    def run(self, env, obj, fieldID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        for annotation in fieldID.annotations:
            if type(annotation) is JfieldIDAnnotation:
                field_name = annotation.field_name
                field_signature = annotation.field_signature
                jni_return_type = get_jni_return_type(field_signature)
                java_return_type = get_java_return_type(field_signature)
                typ = get_type(self.project, java_return_type)
                typ_size = get_type_size(self.project, java_return_type)
                return_value = claripy.BVV(typ.ptr, typ_size)
                for anno in obj.annotations:
                    if type(anno) is JobjectAnnotation:
                        field_exist = False
                        field_index = 0
                        for index, field_info in enumerate(anno.fields_info):
                            if field_info.field_info['field_name'] == field_name and \
                                    field_info.obj_type == jni_return_type:
                                field_exist = True
                                field_index = index
                        if field_exist:
                            return_value = return_value.append_annotation(
                                copy.deepcopy(anno.fields_info[field_index]))
                        else:
                            jni_return_type = get_jni_return_type(field_signature)
                            return_annotation = construct_annotation(jni_return_type, 'from_object')
                            # return_annotation.source = 'from_object'
                            # return_annotation.obj_type = jni_return_type
                            return_annotation.field_info = {'is_field': True, 'field_name': field_name,
                                                            'original_subordinate_obj': anno.source}
                            if anno.source.startswith('arg'):
                                return_annotation.taint_info['is_taint'] = True
                                return_annotation.taint_info['taint_type'] = ['_SOURCE_', '_ARGUMENT_FIELD_']
                                return_annotation.taint_info['taint_info'] = ['SENSITIVE_INFO']
                            return_value = return_value.append_annotation(return_annotation)
                return return_value
        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetObjectField'


class GetBooleanField(angr.SimProcedure):
    def run(self, env, obj, fieldID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jboolean = JBoolean(self.project)
        return_value = claripy.BVV(jboolean.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetBooleanField'


class GetByteField(angr.SimProcedure):
    def run(self, env, obj, fieldID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jbyte = JInt(self.project)
        return_value = claripy.BVV(jbyte.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetByteField'


class GetCharField(angr.SimProcedure):
    def run(self, env, obj, fieldID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jchar = JInt(self.project)
        return_value = claripy.BVV(jchar.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetCharField'


class GetShortField(angr.SimProcedure):
    def run(self, env, obj, fieldID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jshort = JInt(self.project)
        return_value = claripy.BVV(jshort.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetShortField'


class GetIntField(angr.SimProcedure):
    def run(self, env, obj, fieldID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetIntField'


class GetLongField(angr.SimProcedure):
    def run(self, env, obj, fieldID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jlong = JLong(self.project)
        return_value = claripy.BVV(jlong.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetLongField'


class GetFloatField(angr.SimProcedure):
    def run(self, env, obj, fieldID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jfloat = JFloat(self.project)
        return_value = claripy.BVV(jfloat.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetFloatField'


class GetDoubleField(angr.SimProcedure):
    def run(self, env, obj, fieldID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jdouble = JDouble(self.project)
        return_value = claripy.BVV(jdouble.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetDoubleField'


class SetTypeField(angr.SimProcedure):
    def run(self, env, obj, fieldID, value):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'Set<Type>Field'


class SetObjectField(angr.SimProcedure):
    def run(self, env, obj, fieldID, value):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        field_annotation = None
        for annotation in value.annotations:
            if type(annotation) is JobjectAnnotation or type(annotation) is JstringAnnotation or type(
                    annotation) is PrimitiveTypeAnnotation:
                field_annotation = copy.deepcopy(annotation)

        id_annotation = None
        for annotation in fieldID.annotations:
            if type(annotation) is JfieldIDAnnotation:
                id_annotation = annotation
        for annotation in obj.annotations:
            if type(annotation) is JobjectAnnotation:
                field_exist = False
                for index, field_info in enumerate(annotation.fields_info):
                    if field_info.field_name == \
                            id_annotation.field_name and field_info.field_signature == id_annotation.field_signature:
                        field_exist = True
                if field_exist:
                    # TODO need refactor logic
                    pass
                else:
                    field_annotation.field_info['is_field'] = True
                    field_annotation.field_info['field_name'] = id_annotation.field_name
                    field_annotation.field_info['current_subordinate_obj'] = annotation.source
                    annotation.fields_info.append(field_annotation)

    def __repr__(self):
        return 'SetObjectField'


class SetBooleanField(SetTypeField):
    def __repr__(self):
        return 'SetBooleanField'


class SetByteField(SetTypeField):
    def __repr__(self):
        return 'SetByteField'


class SetCharField(SetTypeField):
    def __repr__(self):
        return 'SetCharField'


class SetShortField(SetTypeField):
    def __repr__(self):
        return 'SetShortField'


class SetIntField(SetTypeField):
    def run(self, env, obj, fieldID, value):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        field_annotation = None
        for annotation in value.annotations:
            if type(annotation) is JintAnnotation:
                field_annotation = annotation
        if field_annotation is None:
            field_annotation = JintAnnotation(source='from_native', value=value.ast.args[0])

        id_annotation = None
        for annotation in fieldID.annotations:
            if type(annotation) is JfieldIDAnnotation:
                id_annotation = annotation
        for annotation in obj.annotations:
            if type(annotation) is JobjectAnnotation:
                field_exist = False
                for index, field_info in enumerate(annotation.fields_info):
                    if field_info.field_info['field_name'] == \
                            id_annotation.field_name and \
                            field_info.field_info['field_signature'] == id_annotation.field_signature:
                        field_exist = True
                if field_exist:
                    # TODO need refactor logic
                    pass
                else:
                    field_annotation.field_info['is_field'] = True
                    field_annotation.field_info['field_name'] = id_annotation.field_name
                    field_annotation.field_info['current_subordinate_obj'] = annotation.source
                    annotation.fields_info.append(field_annotation)

    def __repr__(self):
        return 'SetIntField'


class SetLongField(SetTypeField):
    def __repr__(self):
        return 'SetLongField'


class SetFloatField(SetTypeField):
    def __repr__(self):
        return 'SetFloatField'


class SetDoubleField(SetTypeField):
    def __repr__(self):
        return 'SetDoubleField'


class GetStaticMethodID(GetMethodID):
    def __repr__(self):
        return 'GetStaticMethodID'


class CallStaticTypeMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallStatic<Type>Method'


class CallStaticObjectMethod(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticObjectMethod'


class CallStaticObjectMethodV(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticObjectMethodV'


class CallStaticObjectMethodA(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticObjectMethodA'


class CallStaticBooleanMethod(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticBooleanMethod'


class CallStaticBooleanMethodV(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticBooleanMethodV'


class CallStaticBooleanMethodA(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticBooleanMethodA'


class CallStaticByteMethod(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticByteMethod'


class CallStaticByteMethodV(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticByteMethodV'


class CallStaticByteMethodA(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticByteMethodA'


class CallStaticCharMethod(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticCharMethod'


class CallStaticCharMethodV(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticCharMethodV'


class CallStaticCharMethodA(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticCharMethodA'


class CallStaticShortMethod(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticShortMethod'


class CallStaticShortMethodV(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticShortMethodV'


class CallStaticShortMethodA(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticShortMethodA'


class CallStaticIntMethod(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticIntMethod'


class CallStaticIntMethodV(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticIntMethodV'


class CallStaticIntMethodA(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticIntMethodA'


class CallStaticLongMethod(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticLongMethod'


class CallStaticLongMethodV(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticLongMethodV'


class CallStaticLongMethodA(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticLongMethodA'


class CallStaticFloatMethod(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticFloatMethod'


class CallStaticFloatMethodV(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticFloatMethodV'


class CallStaticFloatMethodA(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticFloatMethodA'


class CallStaticDoubleMethod(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticDoubleMethod'


class CallStaticDoubleMethodV(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticDoubleMethodV'


class CallStaticDoubleMethodA(CallStaticTypeMethod):
    def __repr__(self):
        return 'CallStaticDoubleMethodA'


class CallStaticVoidMethod(CallTypeMethod):
    def __repr__(self):
        return 'CallStaticVoidMethod'


class CallStaticVoidMethodV(CallStaticVoidMethod):
    def __repr__(self):
        return 'CallStaticVoidMethodV'


class CallStaticVoidMethodA(CallStaticVoidMethod):
    def __repr__(self):
        return 'CallStaticVoidMethodA'


class GetStaticFieldID(GetFieldID):
    def __repr__(self):
        return 'GetStaticFieldID'


class GetStaticObjectField(GetObjectField):
    def run(self, env, clazz, fieldID):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        for annotation in fieldID.annotations:
            if type(annotation) is JfieldIDAnnotation:
                field_name = annotation.field_name
                field_signature = annotation.field_signature
                java_return_type = get_java_return_type(field_signature)
                typ = get_type(self.project, java_return_type)
                typ_size = get_type_size(self.project, java_return_type)
                return_value = claripy.BVV(typ.ptr, typ_size)
                for anno in clazz.annotations:
                    if type(anno) is JclassAnnotation:
                        field_exist = False
                        field_index = 0
                        for index, field_info in enumerate(anno.fields_info):
                            if field_info.field_info['field_name'] == field_name and \
                                    field_info.obj_type == java_return_type:
                                field_exist = True
                                field_index = index
                        if field_exist:
                            return_value = return_value.append_annotation(
                                copy.deepcopy(anno.fields_info[field_index]))
                        else:
                            jni_return_type = get_jni_return_type(field_signature)
                            return_annotation = construct_annotation(jni_return_type, 'from_class')
                            # return_annotation.source = 'from_class'
                            # return_annotation.obj_type = jni_return_type
                            return_annotation.field_info['is_field'] = True
                            return_annotation.field_info['field_name'] = field_name
                            return_annotation.field_info['original_subordinate_obj'] = anno.class_type

                            return_annotation.taint_info['is_taint'] = True
                            return_annotation.taint_info['taint_type'] = ['_SOURCE_', '_CLASS_FIELD_']
                            return_annotation.taint_info['taint_info'] = ['SENSITIVE_INFO']
                            return_value = return_value.append_annotation(return_annotation)
                return return_value
        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetStaticObjectField'


class GetStaticBooleanField(GetBooleanField):
    def __repr__(self):
        return 'GetStaticBooleanField'


class GetStaticByteField(GetByteField):
    def __repr__(self):
        return 'GetStaticByteField'


class GetStaticCharField(GetCharField):
    def __repr__(self):
        return 'GetStaticCharField'


class GetStaticShortField(GetShortField):
    def __repr__(self):
        return 'GetStaticShortField'


class GetStaticIntField(GetIntField):
    def __repr__(self):
        return 'GetStaticIntField'


class GetStaticLongField(GetLongField):
    def __repr__(self):
        return 'GetStaticLongField'


class GetStaticFloatField(GetFloatField):
    def __repr__(self):
        return 'GetStaticFloatField'


class GetStaticDoubleField(GetDoubleField):
    def __repr__(self):
        return 'GetStaticDoubleField'


class SetStaticObjectField(SetObjectField):
    def __repr__(self):
        return 'SetStaticObjectField'


class SetStaticBooleanField(SetBooleanField):
    def __repr__(self):
        return 'SetStaticBooleanField'


class SetStaticByteField(SetByteField):
    def __repr__(self):
        return 'SetStaticByteField'


class SetStaticCharField(SetCharField):
    def __repr__(self):
        return 'SetStaticCharField'


class SetStaticShortField(SetShortField):
    def __repr__(self):
        return 'SetStaticShortField'


class SetStaticIntField(SetIntField):
    def __repr__(self):
        return 'SetStaticIntField'


class SetStaticLongField(SetLongField):
    def __repr__(self):
        return 'SetStaticLongField'


class SetStaticFloatField(SetFloatField):
    def __repr__(self):
        return 'SetStaticFloatField'


class SetStaticDoubleField(SetDoubleField):
    def __repr__(self):
        return 'SetStaticDoubleField'


class NewString(angr.SimProcedure):
    def run(self, env, unicodeChars, length):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jstring = JString(self.project)
        return_value = claripy.BVV(jstring.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewString'


class GetStringLength(angr.SimProcedure):
    def run(self, env, string):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jsize = JSize(self.project)
        return_value = claripy.BVV(jsize.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetStringLength'


class GetStringChars(angr.SimProcedure):
    def run(self, env, string, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        return string

    def __repr__(self):
        return 'GetStringChars'


class ReleaseStringChars(angr.SimProcedure):
    def run(self, env, string, chars):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseStringChars'


class NewStringUTF(angr.SimProcedure):
    def run(self, env, mybytes):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        strlen_simproc = angr.SIM_PROCEDURES['libc']['strlen']
        name_strlen = self.inline_call(strlen_simproc, mybytes)
        string_arg = self.state.solver.eval(self.state.memory.load(mybytes, name_strlen.ret_expr), cast_to=str)
        nativedroid_logger.info('String: %s', string_arg)

        jstring = JString(self.project)
        return_value = claripy.BVV(jstring.ptr, self.project.arch.bits)
        return_value = return_value.annotate(
            JstringAnnotation(source='from_native', value=string_arg))

        return return_value

    def __repr__(self):
        return 'NewStringUTF'


class GetStringUTFLength(angr.SimProcedure):
    def run(self, env, string):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jsize = JSize(self.project)
        return_value = claripy.BVV(jsize.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetStringUTFLength'


class GetStringUTFChars(angr.SimProcedure):
    def run(self, env, string, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        return string

    def __repr__(self):
        return 'GetStringUTFChars'


class ReleaseStringUTFChars(angr.SimProcedure):
    def run(self, env, string, utf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseStringUTFChars'


class GetArrayLength(angr.SimProcedure):
    def run(self, env, array):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jsize = JSize(self.project)
        return_value = claripy.BVV(jsize.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetArrayLength'


class NewObjectArray(angr.SimProcedure):
    def run(self, env, length, elementClass, initialElement):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject_array = JObjectArray(self.project)
        return_value = claripy.BVV(jobject_array.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewObjectArray'


class GetObjectArrayElement(angr.SimProcedure):
    def run(self, env, arrary, index):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetObjectArrayElement'


class SetObjectArrayElement(angr.SimProcedure):
    def run(self, env, array, index, value):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'SetObjectArrayElement'


class NewBooleanArray(angr.SimProcedure):
    def run(self, env, length):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jboolean_array = JBooleanArray(self.project)
        return_value = claripy.BVV(jboolean_array.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewBooleanArray'


class NewByteArray(angr.SimProcedure):
    def run(self, env, length):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jbyte_array = JByteArray(self.project)
        return_value = claripy.BVV(jbyte_array.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewByteArray'


class NewCharArray(angr.SimProcedure):
    def run(self, env, length):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jchar_array = JCharArray(self.project)
        return_value = claripy.BVV(jchar_array.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewCharArray'


class NewShortArray(angr.SimProcedure):
    def run(self, env, length):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jshort_array = JShortArray(self.project)
        return_value = claripy.BVV(jshort_array.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewShortArray'


class NewIntArray(angr.SimProcedure):
    def run(self, env, length):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint_array = JIntArray(self.project)
        return_value = claripy.BVV(jint_array.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewIntArray'


class NewLongArray(angr.SimProcedure):
    def run(self, env, length):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jlong_array = JLongArray(self.project)
        return_value = claripy.BVV(jlong_array.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewLongArray'


class NewFloatArray(angr.SimProcedure):
    def run(self, env, length):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jfloat_array = JFloatArray(self.project)
        return_value = claripy.BVV(jfloat_array.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewFloatArray'


class NewDoubleArray(angr.SimProcedure):
    def run(self, env, length):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jdouble_array = JDoubleArray(self.project)
        return_value = claripy.BVV(jdouble_array.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewDoubleArray'


class GetBooleanArrayElements(angr.SimProcedure):
    def run(self, env, array, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jsize = JSize(self.project)
        return_value = claripy.BVV(jsize.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetBooleanArrayElements'


class GetByteArrayElements(angr.SimProcedure):
    def run(self, env, array, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        return array

    def __repr__(self):
        return 'GetByteArrayElements'


class GetCharArrayElements(angr.SimProcedure):
    def run(self, env, array, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jsize = JSize(self.project)
        return_value = claripy.BVV(jsize.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetCharArrayElements'


class GetShortArrayElements(angr.SimProcedure):
    def run(self, env, array, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jsize = JSize(self.project)
        return_value = claripy.BVV(jsize.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetShortArrayElements'


class GetIntArrayElements(angr.SimProcedure):
    def run(self, env, array, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jsize = JSize(self.project)
        return_value = claripy.BVV(jsize.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetIntArrayElements'


class GetLongArrayElements(angr.SimProcedure):
    def run(self, env, array, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jsize = JSize(self.project)
        return_value = claripy.BVV(jsize.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetLongArrayElements'


class GetFloatArrayElements(angr.SimProcedure):
    def run(self, env, array, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jsize = JSize(self.project)
        return_value = claripy.BVV(jsize.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetFloatArrayElements'


class GetDoubleArrayElements(angr.SimProcedure):
    def run(self, env, array, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jsize = JSize(self.project)
        return_value = claripy.BVV(jsize.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetDoubleArrayElements'


class ReleaseBooleanArrayElements(angr.SimProcedure):
    def run(self, env, array, elems, mode):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseBooleanArrayElements'


class ReleaseByteArrayElements(angr.SimProcedure):
    def run(self, env, array, elems, mode):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseByteArrayElements'


class ReleaseCharArrayElements(angr.SimProcedure):
    def run(self, env, array, elems, mode):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseCharArrayElements'


class ReleaseShortArrayElements(angr.SimProcedure):
    def run(self, env, array, elems, mode):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseShortArrayElements'


class ReleaseIntArrayElements(angr.SimProcedure):
    def run(self, env, array, elems, mode):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseIntArrayElements'


class ReleaseLongArrayElements(angr.SimProcedure):
    def run(self, env, array, elems, mode):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseLongArrayElements'


class ReleaseFloatArrayElements(angr.SimProcedure):
    def run(self, env, array, elems, mode):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseFloatArrayElements'


class ReleaseDoubleArrayElements(angr.SimProcedure):
    def run(self, env, array, elems, mode):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseDoubleArrayElements'


class GetBooleanArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetBooleanArrayRegion'


class GetByteArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetByteArrayRegion'


class GetCharArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetCharArrayRegion'


class GetShortArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetShortArrayRegion'


class GetIntArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetIntArrayRegion'


class GetLongArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetLongArrayRegion'


class GetFloatArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetFloatArrayRegion'


class GetDoubleArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetDoubleArrayRegion'


class SetBooleanArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'SetBooleanArrayRegion'


class SetByteArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'SetBooleanArrayRegion'


class SetCharArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'SetCharArrayRegion'


class SetShortArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'SetShortArrayRegion'


class SetIntArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'SetIntArrayRegion'


class SetLongArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'SetLongArrayRegion'


class SetFloatArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'SetFloatArrayRegion'


class SetDoubleArrayRegion(angr.SimProcedure):
    def run(self, env, array, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'SetDoubleArrayRegion'


class RegisterNatives(angr.SimProcedure):
    def run(self, env, clazz, methods, nMethods):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        method_num = nMethods.ast.args[0]
        for i in range(method_num):
            method = self.state.mem[methods + i * 3 * self.state.arch.bytes].JNINativeMethod
            name = method.name.deref.string.concrete
            signature = method.signature.deref.string.concrete
            fn_ptr = method.fnPtr.resolved.args[0]
            DYNAMIC_REGISTER_METHODS[(name, signature)] = fn_ptr

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'RegisterNatives'


class UnregisterNatives(angr.SimProcedure):
    def run(self, env, clazz):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'UnregisterNatives'


class MonitorEnter(angr.SimProcedure):
    def run(self, env, obj):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'MonitorEnter'


class MonitorExit(angr.SimProcedure):
    def run(self, env, obj):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'MonitorExit'


class GetJavaVM(angr.SimProcedure):
    def run(self, env, vm):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jint = JInt(self.project)
        return_value = claripy.BVV(jint.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetJavaVM'


class GetStringRegion(angr.SimProcedure):
    def run(self, env, string, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetStringRegion'


class GetStringUTFRegion(angr.SimProcedure):
    def run(self, env, string, start, length, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetStringUTFRegion'


class GetPrimitiveArrayCritical(angr.SimProcedure):
    def run(self, env, array, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetPrimitiveArrayCritical'


class ReleasePrimitiveArrayCritical(angr.SimProcedure):
    def run(self, env, array, carray, mode):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleasePrimitiveArrayCritical'


class GetStringCritical(angr.SimProcedure):
    def run(self, env, string, isCopy):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetStringCritical'


class ReleaseStringCritical(angr.SimProcedure):
    def run(self, env, string, carray):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'ReleaseStringCritical'


class NewWeakGlobalRef(angr.SimProcedure):
    def run(self, env, obj):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jweak = JWeak(self.project)
        return_value = claripy.BVV(jweak.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewWeakGlobalRef'


class DeleteWeakGlobalRef(angr.SimProcedure):
    def run(self, env, obj):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'DeleteWeakGlobalRef'


class ExceptionCheck(angr.SimProcedure):
    def run(self, env):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jboolean = JBoolean(self.project)
        return_value = claripy.BVV(jboolean.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'ExceptionCheck'


class NewDirectByteBuffer(angr.SimProcedure):
    def run(self, env, address, capacity):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject = JObject(self.project)
        return_value = claripy.BVV(jobject.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'NewDirectByteBuffer'


class GetDirectBufferAddress(angr.SimProcedure):
    def run(self, env, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

    def __repr__(self):
        return 'GetDirectBufferAddress'


class GetDirectBufferCapacity(angr.SimProcedure):
    def run(self, env, buf):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jlong = JLong(self.project)
        return_value = claripy.BVV(jlong.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetDirectBufferCapacity'


class GetObjectRefType(angr.SimProcedure):
    def run(self, env, obj):
        nativedroid_logger.info('JNINativeInterface SimProcedure: %s', self)

        jobject_ref_type = JObjectRefType(self.project)
        return_value = claripy.BVV(jobject_ref_type.ptr, self.project.arch.bits)
        return return_value

    def __repr__(self):
        return 'GetObjectRefType'


class JNINativeInterface(ExternObject):
    JNINativeInterface_index_to_name = {
        0: "reserved0",
        1: "reserved1",
        2: "reserved2",
        3: "reserved3",
        4: "GetVersion",
        5: "DefineClass",
        6: "FindClass",
        7: "FromReflectedMethod",
        8: "FromReflectedField",
        9: "ToReflectedMethod",
        10: "GetSuperclass",
        11: "IsAssignableFrom",
        12: "ToReflectedField",
        13: "Throw",
        14: "ThrowNew",
        15: "ExceptionOccurred",
        16: "ExceptionDescribe",
        17: "ExceptionClear",
        18: "FatalError",
        19: "PushLocalFrame",
        20: "PopLocalFrame",
        21: "NewGlobalRef",
        22: "DeleteGlobalRef",
        23: "DeleteLocalRef",
        24: "IsSameObject",
        25: "NewLocalRef",
        26: "EnsureLocalCapacity",
        27: "AllocObject",
        28: "NewObject",
        29: "NewObjectV",
        30: "NewObjectA",
        31: "GetObjectClass",
        32: "IsInstanceOf",
        33: "GetMethodID",
        34: "CallObjectMethod",
        35: "CallObjectMethodV",
        36: "CallObjectMethodA",
        37: "CallBooleanMethod",
        38: "CallBooleanMethodV",
        39: "CallBooleanMethodA",
        40: "CallByteMethod",
        41: "CallByteMethodV",
        42: "CallByteMethodA",
        43: "CallCharMethod",
        44: "CallCharMethodV",
        45: "CallCharMethodA",
        46: "CallShortMethod",
        47: "CallShortMethodV",
        48: "CallShortMethodA",
        49: "CallIntMethod",
        50: "CallIntMethodV",
        51: "CallIntMethodA",
        52: "CallLongMethod",
        53: "CallLongMethodV",
        54: "CallLongMethodA",
        55: "CallFloatMethod",
        56: "CallFloatMethodV",
        57: "CallFloatMethodA",
        58: "CallDoubleMethod",
        59: "CallDoubleMethodV",
        60: "CallDoubleMethodA",
        61: "CallVoidMethod",
        62: "CallVoidMethodV",
        63: "CallVoidMethodA",
        64: "CallNonvirtualObjectMethod",
        65: "CallNonvirtualObjectMethodV",
        66: "CallNonvirtualObjectMethodA",
        67: "CallNonvirtualBooleanMethod",
        68: "CallNonvirtualBooleanMethodV",
        69: "CallNonvirtualBooleanMethodA",
        70: "CallNonvirtualByteMethod",
        71: "CallNonvirtualByteMethodV",
        72: "CallNonvirtualByteMethodA",
        73: "CallNonvirtualCharMethod",
        74: "CallNonvirtualCharMethodV",
        75: "CallNonvirtualCharMethodA",
        76: "CallNonvirtualShortMethod",
        77: "CallNonvirtualShortMethodV",
        78: "CallNonvirtualShortMethodA",
        79: "CallNonvirtualIntMethod",
        80: "CallNonvirtualIntMethodV",
        81: "CallNonvirtualIntMethodA",
        82: "CallNonvirtualLongMethod",
        83: "CallNonvirtualLongMethodV",
        84: "CallNonvirtualLongMethodA",
        85: "CallNonvirtualFloatMethod",
        86: "CallNonvirtualFloatMethodV",
        87: "CallNonvirtualFloatMethodA",
        88: "CallNonvirtualDoubleMethod",
        89: "CallNonvirtualDoubleMethodV",
        90: "CallNonvirtualDoubleMethodA",
        91: "CallNonvirtualVoidMethod",
        92: "CallNonvirtualVoidMethodV",
        93: "CallNonvirtualVoidMethodA",
        94: "GetFieldID",
        95: "GetObjectField",
        96: "GetBooleanField",
        97: "GetByteField",
        98: "GetCharField",
        99: "GetShortField",
        100: "GetIntField",
        101: "GetLongField",
        102: "GetFloatField",
        103: "GetDoubleField",
        104: "SetObjectField",
        105: "SetBooleanField",
        106: "SetByteField",
        107: "SetCharField",
        108: "SetShortField",
        109: "SetIntField",
        110: "SetLongField",
        111: "SetFloatField",
        112: "SetDoubleField",
        113: "GetStaticMethodID",
        114: "CallStaticObjectMethod",
        115: "CallStaticObjectMethodV",
        116: "CallStaticObjectMethodA",
        117: "CallStaticBooleanMethod",
        118: "CallStaticBooleanMethodV",
        119: "CallStaticBooleanMethodA",
        120: "CallStaticByteMethod",
        121: "CallStaticByteMethodV",
        122: "CallStaticByteMethodA",
        123: "CallStaticCharMethod",
        124: "CallStaticCharMethodV",
        125: "CallStaticCharMethodA",
        126: "CallStaticShortMethod",
        127: "CallStaticShortMethodV",
        128: "CallStaticShortMethodA",
        129: "CallStaticIntMethod",
        130: "CallStaticIntMethodV",
        131: "CallStaticIntMethodA",
        132: "CallStaticLongMethod",
        133: "CallStaticLongMethodV",
        134: "CallStaticLongMethodA",
        135: "CallStaticFloatMethod",
        136: "CallStaticFloatMethodV",
        137: "CallStaticFloatMethodA",
        138: "CallStaticDoubleMethod",
        139: "CallStaticDoubleMethodV",
        140: "CallStaticDoubleMethodA",
        141: "CallStaticVoidMethod",
        142: "CallStaticVoidMethodV",
        143: "CallStaticVoidMethodA",
        144: "GetStaticFieldID",
        145: "GetStaticObjectField",
        146: "GetStaticBooleanField",
        147: "GetStaticByteField",
        148: "GetStaticCharField",
        149: "GetStaticShortField",
        150: "GetStaticIntField",
        151: "GetStaticLongField",
        152: "GetStaticFloatField",
        153: "GetStaticDoubleField",
        154: "SetStaticObjectField",
        155: "SetStaticBooleanField",
        156: "SetStaticByteField",
        157: "SetStaticCharField",
        158: "SetStaticShortField",
        159: "SetStaticIntField",
        160: "SetStaticLongField",
        161: "SetStaticFloatField",
        162: "SetStaticDoubleField",
        163: "NewString",
        164: "GetStringLength",
        165: "GetStringChars",
        166: "ReleaseStringChars",
        167: "NewStringUTF",
        168: "GetStringUTFLength",
        169: "GetStringUTFChars",
        170: "ReleaseStringUTFChars",
        171: "GetArrayLength",
        172: "NewObjectArray",
        173: "GetObjectArrayElement",
        174: "SetObjectArrayElement",
        175: "NewBooleanArray",
        176: "NewByteArray",
        177: "NewCharArray",
        178: "NewShortArray",
        179: "NewIntArray",
        180: "NewLongArray",
        181: "NewFloatArray",
        182: "NewDoubleArray",
        183: "GetBooleanArrayElements",
        184: "GetByteArrayElements",
        185: "GetCharArrayElements",
        186: "GetShortArrayElements",
        187: "GetIntArrayElements",
        188: "GetLongArrayElements",
        189: "GetFloatArrayElements",
        190: "GetDoubleArrayElements",
        191: "ReleaseBooleanArrayElements",
        192: "ReleaseByteArrayElements",
        193: "ReleaseCharArrayElements",
        194: "ReleaseShortArrayElements",
        195: "ReleaseIntArrayElements",
        196: "ReleaseLongArrayElements",
        197: "ReleaseFloatArrayElements",
        198: "ReleaseDoubleArrayElements",
        199: "GetBooleanArrayRegion",
        200: "GetByteArrayRegion",
        201: "GetCharArrayRegion",
        202: "GetShortArrayRegion",
        203: "GetIntArrayRegion",
        204: "GetLongArrayRegion",
        205: "GetFloatArrayRegion",
        206: "GetDoubleArrayRegion",
        207: "SetBooleanArrayRegion",
        208: "SetByteArrayRegion",
        209: "SetCharArrayRegion",
        210: "SetShortArrayRegion",
        211: "SetIntArrayRegion",
        212: "SetLongArrayRegion",
        213: "SetFloatArrayRegion",
        214: "SetDoubleArrayRegion",
        215: "RegisterNatives",
        216: "UnregisterNatives",
        217: "MonitorEnter",
        218: "MonitorExit",
        219: "GetJavaVM",
        220: "GetStringRegion",
        221: "GetStringUTFRegion",
        222: "GetPrimitiveArrayCritical",
        223: "ReleasePrimitiveArrayCritical",
        224: "GetStringCritical",
        225: "ReleaseStringCritical",
        226: "NewWeakGlobalRef",
        227: "DeleteWeakGlobalRef",
        228: "ExceptionCheck",
        229: "NewDirectByteBuffer",
        230: "GetDirectBufferAddress",
        231: "GetDirectBufferCapacity",
        232: "GetObjectRefType",
    }
    JNINativeInterface_sig = {
        '_ZN7_JNIEnv10GetVersionEv': 'GetVersion',
        '_ZN7_JNIEnv11DefineClassEPKcP8_jobjectPKai': 'DefineClass',
        '_ZN7_JNIEnv9FindClassEPKc': 'FindClass',
        '_ZN7_JNIEnv19FromReflectedMethodEP8_jobject': 'FromReflectedMethod',
        '_ZN7_JNIEnv18FromReflectedFieldEP8_jobject': 'FromReflectedField',
        '_ZN7_JNIEnv17ToReflectedMethodEP7_jclassP10_jmethodIDh': 'ToReflectedMethod',
        '_ZN7_JNIEnv13GetSuperclassEP7_jclass': 'GetSuperclass',
        '_ZN7_JNIEnv16IsAssignableFromEP7_jclassS1_': 'IsAssignableFrom',
        '_ZN7_JNIEnv16ToReflectedFieldEP7_jclassP9_jfieldIDh': 'ToReflectedField',
        '_ZN7_JNIEnv5ThrowEP11_jthrowable': 'Throw',
        '_ZN7_JNIEnv8ThrowNewEP7_jclassPKc': 'ThrowNew',
        '_ZN7_JNIEnv17ExceptionOccurredEv': 'ExceptionOccurred',
        '_ZN7_JNIEnv17ExceptionDescribeEv': 'ExceptionDescribe',
        '_ZN7_JNIEnv14ExceptionClearEv': 'ExceptionClear',
        '_ZN7_JNIEnv10FatalErrorEPKc': 'FatalError',
        '_ZN7_JNIEnv14PushLocalFrameEi': 'PushLocalFrame',
        '_ZN7_JNIEnv13PopLocalFrameEP8_jobject': 'PopLocalFrame',
        '_ZN7_JNIEnv12NewGlobalRefEP8_jobject': 'NewGlobalRef',
        '_ZN7_JNIEnv15DeleteGlobalRefEP8_jobject': 'DeleteGlobalRef',
        '_ZN7_JNIEnv14DeleteLocalRefEP8_jobject': 'DeleteLocalRef',
        '_ZN7_JNIEnv12IsSameObjectEP8_jobjectS1_': 'IsSameObject',
        '_ZN7_JNIEnv11NewLocalRefEP8_jobject': 'NewLocalRef',
        '_ZN7_JNIEnv19EnsureLocalCapacityEi': 'EnsureLocalCapacity',
        '_ZN7_JNIEnv11AllocObjectEP7_jclass': 'AllocObject',
        '_ZN7_JNIEnv9NewObjectEP7_jclassP10_jmethodIDz': 'NewObject',
        '_ZN7_JNIEnv10NewObjectVEP7_jclassP10_jmethodIDPc': 'NewObjectV',
        '_ZN7_JNIEnv10NewObjectAEP7_jclassP10_jmethodIDP6jvalue': 'NewObjectA',
        '_ZN7_JNIEnv14GetObjectClassEP8_jobject': 'GetObjectClass',
        '_ZN7_JNIEnv12IsInstanceOfEP8_jobjectP7_jclass': 'IsInstanceOf',
        '_ZN7_JNIEnv11GetMethodIDEP7_jclassPKcS3_': 'GetMethodID',
        '_ZN7_JNIEnv16CallObjectMethodEP8_jobjectP10_jmethodIDz': 'CallObjectMethod',
        '_ZN7_JNIEnv17CallObjectMethodVEP8_jobjectP10_jmethodIDPc': 'CallObjectMethodV',
        '_ZN7_JNIEnv17CallObjectMethodAEP8_jobjectP10_jmethodIDP6jvalue': 'CallObjectMethodA',
        '_ZN7_JNIEnv17CallBooleanMethodEP8_jobjectP10_jmethodIDz': 'CallBooleanMethod',
        '_ZN7_JNIEnv18CallBooleanMethodVEP8_jobjectP10_jmethodIDPc': 'CallBooleanMethodV',
        '_ZN7_JNIEnv18CallBooleanMethodAEP8_jobjectP10_jmethodIDP6jvalue': 'CallBooleanMethodA',
        '_ZN7_JNIEnv14CallByteMethodEP8_jobjectP10_jmethodIDz': 'CallByteMethod',
        '_ZN7_JNIEnv15CallByteMethodVEP8_jobjectP10_jmethodIDPc': 'CallByteMethodV',
        '_ZN7_JNIEnv15CallByteMethodAEP8_jobjectP10_jmethodIDP6jvalue': 'CallByteMethodA',
        '_ZN7_JNIEnv14CallCharMethodEP8_jobjectP10_jmethodIDz': 'CallCharMethod',
        '_ZN7_JNIEnv15CallCharMethodVEP8_jobjectP10_jmethodIDPc': 'CallCharMethodV',
        '_ZN7_JNIEnv15CallCharMethodAEP8_jobjectP10_jmethodIDP6jvalue': 'CallCharMethodA',
        '_ZN7_JNIEnv15CallShortMethodEP8_jobjectP10_jmethodIDz': 'CallShortMethod',
        '_ZN7_JNIEnv16CallShortMethodVEP8_jobjectP10_jmethodIDPc': 'CallShortMethodV',
        '_ZN7_JNIEnv16CallShortMethodAEP8_jobjectP10_jmethodIDP6jvalue': 'CallShortMethodA',
        '_ZN7_JNIEnv13CallIntMethodEP8_jobjectP10_jmethodIDz': 'CallIntMethod',
        '_ZN7_JNIEnv14CallIntMethodVEP8_jobjectP10_jmethodIDPc': 'CallIntMethodV',
        '_ZN7_JNIEnv14CallIntMethodAEP8_jobjectP10_jmethodIDP6jvalue': 'CallIntMethodA',
        '_ZN7_JNIEnv14CallLongMethodEP8_jobjectP10_jmethodIDz': 'CallLongMethod',
        '_ZN7_JNIEnv15CallLongMethodVEP8_jobjectP10_jmethodIDPc': 'CallLongMethodV',
        '_ZN7_JNIEnv15CallLongMethodAEP8_jobjectP10_jmethodIDP6jvalue': 'CallLongMethodA',
        '_ZN7_JNIEnv15CallFloatMethodEP8_jobjectP10_jmethodIDz': 'CallFloatMethod',
        '_ZN7_JNIEnv16CallFloatMethodVEP8_jobjectP10_jmethodIDPc': 'CallFloatMethodV',
        '_ZN7_JNIEnv16CallFloatMethodAEP8_jobjectP10_jmethodIDP6jvalue': 'CallFloatMethodA',
        '_ZN7_JNIEnv16CallDoubleMethodEP8_jobjectP10_jmethodIDz': 'CallDoubleMethod',
        '_ZN7_JNIEnv17CallDoubleMethodVEP8_jobjectP10_jmethodIDPc': 'CallDoubleMethodV',
        '_ZN7_JNIEnv17CallDoubleMethodAEP8_jobjectP10_jmethodIDP6jvalue': 'CallDoubleMethodA',
        '_ZN7_JNIEnv14CallVoidMethodEP8_jobjectP10_jmethodIDz': 'CallVoidMethod',
        '_ZN7_JNIEnv15CallVoidMethodVEP8_jobjectP10_jmethodIDPc': 'CallVoidMethodV',
        '_ZN7_JNIEnv15CallVoidMethodAEP8_jobjectP10_jmethodIDP6jvalue': 'CallVoidMethodA',
        '_ZN7_JNIEnv26CallNonvirtualObjectMethodEP8_jobjectP7_jclassP10_jmethodIDz': 'CallNonvirtualObjectMethod',
        '_ZN7_JNIEnv27CallNonvirtualObjectMethodVEP8_jobjectP7_jclassP10_jmethodIDPc': 'CallNonvirtualObjectMethodV',
        '_ZN7_JNIEnv27CallNonvirtualObjectMethodAEP8_jobjectP7_jclassP10_jmethodIDP6jvalue':
            'CallNonvirtualObjectMethodA',
        '_ZN7_JNIEnv27CallNonvirtualBooleanMethodEP8_jobjectP7_jclassP10_jmethodIDz': 'CallNonvirtualBooleanMethod',
        '_ZN7_JNIEnv28CallNonvirtualBooleanMethodVEP8_jobjectP7_jclassP10_jmethodIDPc': 'CallNonvirtualBooleanMethodV',
        '_ZN7_JNIEnv28CallNonvirtualBooleanMethodAEP8_jobjectP7_jclassP10_jmethodIDP6jvalue':
            'CallNonvirtualBooleanMethodA',
        '_ZN7_JNIEnv24CallNonvirtualByteMethodEP8_jobjectP7_jclassP10_jmethodIDz': 'CallNonvirtualByteMethod',
        '_ZN7_JNIEnv25CallNonvirtualByteMethodVEP8_jobjectP7_jclassP10_jmethodIDPc': 'CallNonvirtualByteMethodV',
        '_ZN7_JNIEnv25CallNonvirtualByteMethodAEP8_jobjectP7_jclassP10_jmethodIDP6jvalue': 'CallNonvirtualByteMethodA',
        '_ZN7_JNIEnv24CallNonvirtualCharMethodEP8_jobjectP7_jclassP10_jmethodIDz': 'CallNonvirtualCharMethod',
        '_ZN7_JNIEnv25CallNonvirtualCharMethodVEP8_jobjectP7_jclassP10_jmethodIDPc': 'CallNonvirtualCharMethodV',
        '_ZN7_JNIEnv25CallNonvirtualCharMethodAEP8_jobjectP7_jclassP10_jmethodIDP6jvalue': 'CallNonvirtualCharMethodA',
        '_ZN7_JNIEnv25CallNonvirtualShortMethodEP8_jobjectP7_jclassP10_jmethodIDz': 'CallNonvirtualShortMethod',
        '_ZN7_JNIEnv26CallNonvirtualShortMethodVEP8_jobjectP7_jclassP10_jmethodIDPc': 'CallNonvirtualShortMethodV',
        '_ZN7_JNIEnv26CallNonvirtualShortMethodAEP8_jobjectP7_jclassP10_jmethodIDP6jvalue':
            'CallNonvirtualShortMethodA',
        '_ZN7_JNIEnv23CallNonvirtualIntMethodEP8_jobjectP7_jclassP10_jmethodIDz': 'CallNonvirtualIntMethod',
        '_ZN7_JNIEnv24CallNonvirtualIntMethodVEP8_jobjectP7_jclassP10_jmethodIDPc': 'CallNonvirtualIntMethodV',
        '_ZN7_JNIEnv24CallNonvirtualIntMethodAEP8_jobjectP7_jclassP10_jmethodIDP6jvalue': 'CallNonvirtualIntMethodA',
        '_ZN7_JNIEnv24CallNonvirtualLongMethodEP8_jobjectP7_jclassP10_jmethodIDz': 'CallNonvirtualLongMethod',
        '_ZN7_JNIEnv25CallNonvirtualLongMethodVEP8_jobjectP7_jclassP10_jmethodIDPc': 'CallNonvirtualLongMethodV',
        '_ZN7_JNIEnv25CallNonvirtualLongMethodAEP8_jobjectP7_jclassP10_jmethodIDP6jvalue': 'CallNonvirtualLongMethodA',
        '_ZN7_JNIEnv25CallNonvirtualFloatMethodEP8_jobjectP7_jclassP10_jmethodIDz': 'CallNonvirtualFloatMethod',
        '_ZN7_JNIEnv26CallNonvirtualFloatMethodVEP8_jobjectP7_jclassP10_jmethodIDPc': 'CallNonvirtualFloatMethodV',
        '_ZN7_JNIEnv26CallNonvirtualFloatMethodAEP8_jobjectP7_jclassP10_jmethodIDP6jvalue':
            'CallNonvirtualFloatMethodA',
        '_ZN7_JNIEnv26CallNonvirtualDoubleMethodEP8_jobjectP7_jclassP10_jmethodIDz': 'CallNonvirtualDoubleMethod',
        '_ZN7_JNIEnv27CallNonvirtualDoubleMethodVEP8_jobjectP7_jclassP10_jmethodIDPc': 'CallNonvirtualDoubleMethodV',
        '_ZN7_JNIEnv27CallNonvirtualDoubleMethodAEP8_jobjectP7_jclassP10_jmethodIDP6jvalue':
            'CallNonvirtualDoubleMethodA',
        '_ZN7_JNIEnv24CallNonvirtualVoidMethodEP8_jobjectP7_jclassP10_jmethodIDz': 'CallNonvirtualVoidMethod',
        '_ZN7_JNIEnv25CallNonvirtualVoidMethodVEP8_jobjectP7_jclassP10_jmethodIDPc': 'CallNonvirtualVoidMethodV',
        '_ZN7_JNIEnv25CallNonvirtualVoidMethodAEP8_jobjectP7_jclassP10_jmethodIDP6jvalue': 'CallNonvirtualVoidMethodA',
        '_ZN7_JNIEnv10GetFieldIDEP7_jclassPKcS3_': 'GetFieldID',
        '_ZN7_JNIEnv14GetObjectFieldEP8_jobjectP9_jfieldID': 'GetObjectField',
        '_ZN7_JNIEnv15GetBooleanFieldEP8_jobjectP9_jfieldID': 'GetBooleanField',
        '_ZN7_JNIEnv12GetByteFieldEP8_jobjectP9_jfieldID': 'GetByteField',
        '_ZN7_JNIEnv12GetCharFieldEP8_jobjectP9_jfieldID': 'GetCharField',
        '_ZN7_JNIEnv13GetShortFieldEP8_jobjectP9_jfieldID': 'GetShortField',
        '_ZN7_JNIEnv11GetIntFieldEP8_jobjectP9_jfieldID': 'GetIntField',
        '_ZN7_JNIEnv12GetLongFieldEP8_jobjectP9_jfieldID': 'GetLongField',
        '_ZN7_JNIEnv13GetFloatFieldEP8_jobjectP9_jfieldID': 'GetFloatField',
        '_ZN7_JNIEnv14GetDoubleFieldEP8_jobjectP9_jfieldID': 'GetDoubleField',
        '_ZN7_JNIEnv14SetObjectFieldEP8_jobjectP9_jfieldIDS1_': 'SetObjectField',
        '_ZN7_JNIEnv15SetBooleanFieldEP8_jobjectP9_jfieldIDh': 'SetBooleanField',
        '_ZN7_JNIEnv12SetByteFieldEP8_jobjectP9_jfieldIDa': 'SetByteField',
        '_ZN7_JNIEnv12SetCharFieldEP8_jobjectP9_jfieldIDt': 'SetCharField',
        '_ZN7_JNIEnv13SetShortFieldEP8_jobjectP9_jfieldIDs': 'SetShortField',
        '_ZN7_JNIEnv11SetIntFieldEP8_jobjectP9_jfieldIDi': 'SetIntField',
        '_ZN7_JNIEnv12SetLongFieldEP8_jobjectP9_jfieldIDx': 'SetLongField',
        '_ZN7_JNIEnv13SetFloatFieldEP8_jobjectP9_jfieldIDf': 'SetFloatField',
        '_ZN7_JNIEnv14SetDoubleFieldEP8_jobjectP9_jfieldIDd': 'SetDoubleField',
        '_ZN7_JNIEnv17GetStaticMethodIDEP7_jclassPKcS3_': 'GetStaticMethodID',
        '_ZN7_JNIEnv22CallStaticObjectMethodEP7_jclassP10_jmethodIDz': 'CallStaticObjectMethod',
        '_ZN7_JNIEnv23CallStaticObjectMethodVEP7_jclassP10_jmethodIDPc': 'CallStaticObjectMethodV',
        '_ZN7_JNIEnv23CallStaticObjectMethodAEP7_jclassP10_jmethodIDP6jvalue': 'CallStaticObjectMethodA',
        '_ZN7_JNIEnv23CallStaticBooleanMethodEP7_jclassP10_jmethodIDz': 'CallStaticBooleanMethod',
        '_ZN7_JNIEnv24CallStaticBooleanMethodVEP7_jclassP10_jmethodIDPc': 'CallStaticBooleanMethodV',
        '_ZN7_JNIEnv24CallStaticBooleanMethodAEP7_jclassP10_jmethodIDP6jvalue': 'CallStaticBooleanMethodA',
        '_ZN7_JNIEnv20CallStaticByteMethodEP7_jclassP10_jmethodIDz': 'CallStaticByteMethod',
        '_ZN7_JNIEnv21CallStaticByteMethodVEP7_jclassP10_jmethodIDPc': 'CallStaticByteMethodV',
        '_ZN7_JNIEnv21CallStaticByteMethodAEP7_jclassP10_jmethodIDP6jvalue': 'CallStaticByteMethodA',
        '_ZN7_JNIEnv20CallStaticCharMethodEP7_jclassP10_jmethodIDz': 'CallStaticCharMethod',
        '_ZN7_JNIEnv21CallStaticCharMethodVEP7_jclassP10_jmethodIDPc': 'CallStaticCharMethodV',
        '_ZN7_JNIEnv21CallStaticCharMethodAEP7_jclassP10_jmethodIDP6jvalue': 'CallStaticCharMethodA',
        '_ZN7_JNIEnv21CallStaticShortMethodEP7_jclassP10_jmethodIDz': 'CallStaticShortMethod',
        '_ZN7_JNIEnv22CallStaticShortMethodVEP7_jclassP10_jmethodIDPc': 'CallStaticShortMethodV',
        '_ZN7_JNIEnv22CallStaticShortMethodAEP7_jclassP10_jmethodIDP6jvalue': 'CallStaticShortMethodA',
        '_ZN7_JNIEnv19CallStaticIntMethodEP7_jclassP10_jmethodIDz': 'CallStaticIntMethod',
        '_ZN7_JNIEnv20CallStaticIntMethodVEP7_jclassP10_jmethodIDPc': 'CallStaticIntMethodV',
        '_ZN7_JNIEnv20CallStaticIntMethodAEP7_jclassP10_jmethodIDP6jvalue': 'CallStaticIntMethodA',
        '_ZN7_JNIEnv20CallStaticLongMethodEP7_jclassP10_jmethodIDz': 'CallStaticLongMethod',
        '_ZN7_JNIEnv21CallStaticLongMethodVEP7_jclassP10_jmethodIDPc': 'CallStaticLongMethodV',
        '_ZN7_JNIEnv21CallStaticLongMethodAEP7_jclassP10_jmethodIDP6jvalue': 'CallStaticLongMethodA',
        '_ZN7_JNIEnv21CallStaticFloatMethodEP7_jclassP10_jmethodIDz': 'CallStaticFloatMethod',
        '_ZN7_JNIEnv22CallStaticFloatMethodVEP7_jclassP10_jmethodIDPc': 'CallStaticFloatMethodV',
        '_ZN7_JNIEnv22CallStaticFloatMethodAEP7_jclassP10_jmethodIDP6jvalue': 'CallStaticFloatMethodA',
        '_ZN7_JNIEnv22CallStaticDoubleMethodEP7_jclassP10_jmethodIDz': 'CallStaticDoubleMethod',
        '_ZN7_JNIEnv23CallStaticDoubleMethodVEP7_jclassP10_jmethodIDPc': 'CallStaticDoubleMethodV',
        '_ZN7_JNIEnv23CallStaticDoubleMethodAEP7_jclassP10_jmethodIDP6jvalue': 'CallStaticDoubleMethodA',
        '_ZN7_JNIEnv20CallStaticVoidMethodEP7_jclassP10_jmethodIDz': 'CallStaticVoidMethod',
        '_ZN7_JNIEnv21CallStaticVoidMethodVEP7_jclassP10_jmethodIDPc': 'CallStaticVoidMethodV',
        '_ZN7_JNIEnv21CallStaticVoidMethodAEP7_jclassP10_jmethodIDP6jvalue': 'CallStaticVoidMethodA',
        '_ZN7_JNIEnv16GetStaticFieldIDEP7_jclassPKcS3_': 'GetStaticFieldID',
        '_ZN7_JNIEnv20GetStaticObjectFieldEP7_jclassP9_jfieldID': 'GetStaticObjectField',
        '_ZN7_JNIEnv21GetStaticBooleanFieldEP7_jclassP9_jfieldID': 'GetStaticBooleanField',
        '_ZN7_JNIEnv18GetStaticByteFieldEP7_jclassP9_jfieldID': 'GetStaticByteField',
        '_ZN7_JNIEnv18GetStaticCharFieldEP7_jclassP9_jfieldID': 'GetStaticCharField',
        '_ZN7_JNIEnv19GetStaticShortFieldEP7_jclassP9_jfieldID': 'GetStaticShortField',
        '_ZN7_JNIEnv17GetStaticIntFieldEP7_jclassP9_jfieldID': 'GetStaticIntField',
        '_ZN7_JNIEnv18GetStaticLongFieldEP7_jclassP9_jfieldID': 'GetStaticLongField',
        '_ZN7_JNIEnv19GetStaticFloatFieldEP7_jclassP9_jfieldID': 'GetStaticFloatField',
        '_ZN7_JNIEnv20GetStaticDoubleFieldEP7_jclassP9_jfieldID': 'GetStaticDoubleField',
        '_ZN7_JNIEnv20SetStaticObjectFieldEP7_jclassP9_jfieldIDP8_jobject': 'SetStaticObjectField',
        '_ZN7_JNIEnv21SetStaticBooleanFieldEP7_jclassP9_jfieldIDh': 'SetStaticBooleanField',
        '_ZN7_JNIEnv18SetStaticByteFieldEP7_jclassP9_jfieldIDa': 'SetStaticByteField',
        '_ZN7_JNIEnv18SetStaticCharFieldEP7_jclassP9_jfieldIDt': 'SetStaticCharField',
        '_ZN7_JNIEnv19SetStaticShortFieldEP7_jclassP9_jfieldIDs': 'SetStaticShortField',
        '_ZN7_JNIEnv17SetStaticIntFieldEP7_jclassP9_jfieldIDi': 'SetStaticIntField',
        '_ZN7_JNIEnv18SetStaticLongFieldEP7_jclassP9_jfieldIDx': 'SetStaticLongField',
        '_ZN7_JNIEnv19SetStaticFloatFieldEP7_jclassP9_jfieldIDf': 'SetStaticFloatField',
        '_ZN7_JNIEnv20SetStaticDoubleFieldEP7_jclassP9_jfieldIDd': 'SetStaticDoubleField',
        '_ZN7_JNIEnv9NewStringEPKti': 'NewString',
        '_ZN7_JNIEnv15GetStringLengthEP8_jstring': 'GetStringLength',
        '_ZN7_JNIEnv14GetStringCharsEP8_jstringPh': 'GetStringChars',
        '_ZN7_JNIEnv18ReleaseStringCharsEP8_jstringPKt': 'ReleaseStringChars',
        '_ZN7_JNIEnv12NewStringUTFEPKc': 'NewStringUTF',
        '_ZN7_JNIEnv18GetStringUTFLengthEP8_jstring': 'GetStringUTFLength',
        '_ZN7_JNIEnv17GetStringUTFCharsEP8_jstringPh': 'GetStringUTFChars',
        '_ZN7_JNIEnv21ReleaseStringUTFCharsEP8_jstringPKc': 'ReleaseStringUTFChars',
        '_ZN7_JNIEnv14GetArrayLengthEP7_jarray': 'GetArrayLength',
        '_ZN7_JNIEnv14NewObjectArrayEiP7_jclassP8_jobject': 'NewObjectArray',
        '_ZN7_JNIEnv21GetObjectArrayElementEP13_jobjectArrayi': 'GetObjectArrayElement',
        '_ZN7_JNIEnv21SetObjectArrayElementEP13_jobjectArrayiP8_jobject': 'SetObjectArrayElement',
        '_ZN7_JNIEnv15NewBooleanArrayEi': 'NewBooleanArray',
        '_ZN7_JNIEnv12NewByteArrayEi': 'NewByteArray',
        '_ZN7_JNIEnv12NewCharArrayEi': 'NewCharArray',
        '_ZN7_JNIEnv13NewShortArrayEi': 'NewShortArray',
        '_ZN7_JNIEnv11NewIntArrayEi': 'NewIntArray',
        '_ZN7_JNIEnv12NewLongArrayEi': 'NewLongArray',
        '_ZN7_JNIEnv13NewFloatArrayEi': 'NewFloatArray',
        '_ZN7_JNIEnv14NewDoubleArrayEi': 'NewDoubleArray',
        '_ZN7_JNIEnv23GetBooleanArrayElementsEP14_jbooleanArrayPh': 'GetBooleanArrayElements',
        '_ZN7_JNIEnv20GetByteArrayElementsEP11_jbyteArrayPh': 'GetByteArrayElements',
        '_ZN7_JNIEnv20GetCharArrayElementsEP11_jcharArrayPh': 'GetCharArrayElements',
        '_ZN7_JNIEnv21GetShortArrayElementsEP12_jshortArrayPh': 'GetShortArrayElements',
        '_ZN7_JNIEnv19GetIntArrayElementsEP10_jintArrayPh': 'GetIntArrayElements',
        '_ZN7_JNIEnv20GetLongArrayElementsEP11_jlongArrayPh': 'GetLongArrayElements',
        '_ZN7_JNIEnv21GetFloatArrayElementsEP12_jfloatArrayPh': 'GetFloatArrayElements',
        '_ZN7_JNIEnv22GetDoubleArrayElementsEP13_jdoubleArrayPh': 'GetDoubleArrayElements',
        '_ZN7_JNIEnv27ReleaseBooleanArrayElementsEP14_jbooleanArrayPhi': 'ReleaseBooleanArrayElements',
        '_ZN7_JNIEnv24ReleaseByteArrayElementsEP11_jbyteArrayPai': 'ReleaseByteArrayElements',
        '_ZN7_JNIEnv24ReleaseCharArrayElementsEP11_jcharArrayPti': 'ReleaseCharArrayElements',
        '_ZN7_JNIEnv25ReleaseShortArrayElementsEP12_jshortArrayPsi': 'ReleaseShortArrayElements',
        '_ZN7_JNIEnv23ReleaseIntArrayElementsEP10_jintArrayPii': 'ReleaseIntArrayElements',
        '_ZN7_JNIEnv24ReleaseLongArrayElementsEP11_jlongArrayPxi': 'ReleaseLongArrayElements',
        '_ZN7_JNIEnv25ReleaseFloatArrayElementsEP12_jfloatArrayPfi': 'ReleaseFloatArrayElements',
        '_ZN7_JNIEnv26ReleaseDoubleArrayElementsEP13_jdoubleArrayPdi': 'ReleaseDoubleArrayElements',
        '_ZN7_JNIEnv21GetBooleanArrayRegionEP14_jbooleanArrayiiPh': 'GetBooleanArrayRegion',
        '_ZN7_JNIEnv18GetByteArrayRegionEP11_jbyteArrayiiPa': 'GetByteArrayRegion',
        '_ZN7_JNIEnv18GetCharArrayRegionEP11_jcharArrayiiPt': 'GetCharArrayRegion',
        '_ZN7_JNIEnv19GetShortArrayRegionEP12_jshortArrayiiPs': 'GetShortArrayRegion',
        '_ZN7_JNIEnv17GetIntArrayRegionEP10_jintArrayiiPi': 'GetIntArrayRegion',
        '_ZN7_JNIEnv18GetLongArrayRegionEP11_jlongArrayiiPx': 'GetLongArrayRegion',
        '_ZN7_JNIEnv19GetFloatArrayRegionEP12_jfloatArrayiiPf': 'GetFloatArrayRegion',
        '_ZN7_JNIEnv20GetDoubleArrayRegionEP13_jdoubleArrayiiPd': 'GetDoubleArrayRegion',
        '_ZN7_JNIEnv21SetBooleanArrayRegionEP14_jbooleanArrayiiPKh': 'SetBooleanArrayRegion',
        '_ZN7_JNIEnv18SetByteArrayRegionEP11_jbyteArrayiiPKa': 'SetByteArrayRegion',
        '_ZN7_JNIEnv18SetCharArrayRegionEP11_jcharArrayiiPKt': 'SetCharArrayRegion',
        '_ZN7_JNIEnv19SetShortArrayRegionEP12_jshortArrayiiPKs': 'SetShortArrayRegion',
        '_ZN7_JNIEnv17SetIntArrayRegionEP10_jintArrayiiPKi': 'SetIntArrayRegion',
        '_ZN7_JNIEnv18SetLongArrayRegionEP11_jlongArrayiiPKx': 'SetLongArrayRegion',
        '_ZN7_JNIEnv19SetFloatArrayRegionEP12_jfloatArrayiiPKf': 'SetFloatArrayRegion',
        '_ZN7_JNIEnv20SetDoubleArrayRegionEP13_jdoubleArrayiiPKd': 'SetDoubleArrayRegion',
        '_ZN7_JNIEnv15RegisterNativesEP7_jclassPK15JNINativeMethodi': 'RegisterNatives',
        '_ZN7_JNIEnv17UnregisterNativesEP7_jclass': 'UnregisterNatives',
        '_ZN7_JNIEnv12MonitorEnterEP8_jobject': 'MonitorEnter',
        '_ZN7_JNIEnv11MonitorExitEP8_jobject': 'MonitorExit',
        '_ZN7_JNIEnv9GetJavaVMEPP7_JavaVM': 'GetJavaVM',
        '_ZN7_JNIEnv15GetStringRegionEP8_jstringiiPt': 'GetStringRegion',
        '_ZN7_JNIEnv18GetStringUTFRegionEP8_jstringiiPc': 'GetStringUTFRegion',
        '_ZN7_JNIEnv25GetPrimitiveArrayCriticalEP7_jarrayPh': 'GetPrimitiveArrayCritical',
        '_ZN7_JNIEnv29ReleasePrimitiveArrayCriticalEP7_jarrayPvi': 'ReleasePrimitiveArrayCritical',
        '_ZN7_JNIEnv17GetStringCriticalEP8_jstringPh': 'GetStringCritical',
        '_ZN7_JNIEnv21ReleaseStringCriticalEP8_jstringPKt': 'ReleaseStringCritical',
        '_ZN7_JNIEnv16NewWeakGlobalRefEP8_jobject': 'NewWeakGlobalRef',
        '_ZN7_JNIEnv19DeleteWeakGlobalRefEP8_jobject': 'DeleteWeakGlobalRef',
        '_ZN7_JNIEnv14ExceptionCheckEv': 'ExceptionCheck',
        '_ZN7_JNIEnv19NewDirectByteBufferEPvx': 'NewDirectByteBuffer',
        '_ZN7_JNIEnv22GetDirectBufferAddressEP8_jobject': 'GetDirectBufferAddress',
        '_ZN7_JNIEnv23GetDirectBufferCapacityEP8_jobject': 'GetDirectBufferCapacity',
        '_ZN7_JNIEnv16GetObjectRefTypeEP8_jobject': 'GetObjectRefType',

    }
    JNINativeInterface_name_to_simproc = {
        'GetVersion': GetVersion,
        'DefineClass': DefineClass,
        'FindClass': FindClass,
        'FromReflectedMethod': FromReflectedMethod,
        'FromReflectedField': FromReflectedField,
        'ToReflectedMethod': ToReflectedMethod,
        'GetSuperClass': GetSuperClass,
        'IsAssignableFrom': IsAssignableFrom,
        'ToReflectedField': ToReflectedField,
        'Throw': Throw,
        'ThrowNew': ThrowNew,
        'ExceptionOccurred': ExceptionOccurred,
        'ExceptionDescribe': ExceptionDescribe,
        'ExceptionClear': ExceptionClear,
        'FatalError': FatalError,
        'PushLocalFrame': PushLocalFrame,
        'PopLocalFrame': PopLocalFrame,
        'NewGlobalRef': NewGlobalRef,
        'DeleteGlobalRef': DeleteGlobalRef,
        'DeleteLocalRef': DeleteLocalRef,
        'IsSameObject': IsSameObject,
        'NewLocalRef': NewLocalRef,
        'EnsureLocalCapacity': EnsureLocalCapacity,
        'AllocObject': AllocObject,
        'NewObject': NewObject,
        'NewObjectV': NewObjectV,
        'NewObjectA': NewObjectA,
        'GetObjectClass': GetObjectClass,
        'IsInstanceOf': IsInstanceOf,
        'GetMethodID': GetMethodID,
        'CallObjectMethod': CallObjectMethod,
        'CallObjectMethodV': CallObjectMethodV,
        'CallObjectMethodA': CallObjectMethodA,
        'CallBooleanMethod': CallBooleanMethod,
        'CallBooleanMethodV': CallBooleanMethodV,
        'CallBooleanMethodA': CallBooleanMethodA,
        'CallByteMethod': CallByteMethod,
        'CallByteMethodV': CallByteMethodV,
        'CallByteMethodA': CallByteMethodA,
        'CallCharMethod': CallCharMethod,
        'CallCharMethodV': CallCharMethodV,
        'CallCharMethodA': CallCharMethodA,
        'CallShortMethod': CallShortMethod,
        'CallShortMethodV': CallShortMethodV,
        'CallShortMethodA': CallShortMethodA,
        'CallIntMethod': CallIntMethod,
        'CallIntMethodV': CallIntMethodV,
        'CallIntMethodA': CallIntMethodA,
        'CallLongMethod': CallLongMethod,
        'CallLongMethodV': CallLongMethodV,
        'CallLongMethodA': CallLongMethodA,
        'CallFloatMethod': CallFloatMethod,
        'CallFloatMethodV': CallFloatMethodV,
        'CallFloatMethodA': CallFloatMethodA,
        'CallDoubleMethod': CallDoubleMethod,
        'CallDoubleMethodV': CallDoubleMethodV,
        'CallDoubleMethodA': CallDoubleMethodA,
        'CallVoidMethod': CallVoidMethod,
        'CallVoidMethodV': CallVoidMethodV,
        'CallVoidMethodA': CallVoidMethodA,
        'CallNonvirtualObjectMethod': CallNonvirtualObjectMethod,
        'CallNonvirtualObjectMethodV': CallNonvirtualObjectMethodV,
        'CallNonvirtualObjectMethodA': CallNonvirtualObjectMethodA,
        'CallNonvirtualBooleanMethod': CallNonvirtualBooleanMethod,
        'CallNonvirtualBooleanMethodV': CallNonvirtualBooleanMethodV,
        'CallNonvirtualBooleanMethodA': CallNonvirtualBooleanMethodA,
        'CallNonvirtualByteMethod': CallNonvirtualByteMethod,
        'CallNonvirtualByteMethodV': CallNonvirtualByteMethodV,
        'CallNonvirtualByteMethodA': CallNonvirtualByteMethodA,
        'CallNonvirtualCharMethod': CallNonvirtualCharMethod,
        'CallNonvirtualCharMethodV': CallNonvirtualCharMethodV,
        'CallNonvirtualCharMethodA': CallNonvirtualCharMethodA,
        'CallNonvirtualShortMethod': CallNonvirtualShortMethod,
        'CallNonvirtualShortMethodV': CallNonvirtualShortMethodV,
        'CallNonvirtualShortMethodA': CallNonvirtualShortMethodA,
        'CallNonvirtualIntMethod': CallNonvirtualIntMethod,
        'CallNonvirtualIntMethodV': CallNonvirtualIntMethodV,
        'CallNonvirtualIntMethodA': CallNonvirtualIntMethodA,
        'CallNonvirtualLongMethod': CallNonvirtualLongMethod,
        'CallNonvirtualLongMethodV': CallNonvirtualLongMethodV,
        'CallNonvirtualLongMethodA': CallNonvirtualLongMethodA,
        'CallNonvirtualFloatMethod': CallNonvirtualFloatMethod,
        'CallNonvirtualFloatMethodV': CallNonvirtualFloatMethodV,
        'CallNonvirtualFloatMethodA': CallNonvirtualFloatMethodA,
        'CallNonvirtualDoubleMethod': CallNonvirtualDoubleMethod,
        'CallNonvirtualDoubleMethodV': CallNonvirtualDoubleMethodV,
        'CallNonvirtualDoubleMethodA': CallNonvirtualDoubleMethodA,
        'CallNonvirtualVoidMethod': CallNonvirtualVoidMethod,
        'CallNonvirtualVoidMethodV': CallNonvirtualVoidMethodV,
        'CallNonvirtualVoidMethodA': CallNonvirtualVoidMethodA,
        'GetFieldID': GetFieldID,
        'GetObjectField': GetObjectField,
        'GetBooleanField': GetBooleanField,
        'GetByteField': GetByteField,
        'GetCharField': GetCharField,
        'GetShortField': GetShortField,
        'GetIntField': GetIntField,
        'GetLongField': GetLongField,
        'GetFloatField': GetFloatField,
        'GetDoubleField': GetDoubleField,
        'SetObjectField': SetObjectField,
        'SetBooleanField': SetBooleanField,
        'SetByteField': SetByteField,
        'SetCharField': SetCharField,
        'SetShortField': SetShortField,
        'SetIntField': SetIntField,
        'SetLongField': SetLongField,
        'SetFloatField': SetFloatField,
        'SetDoubleField': SetDoubleField,
        'GetStaticMethodID': GetStaticMethodID,
        'CallStaticObjectMethod': CallStaticObjectMethod,
        'CallStaticObjectMethodV': CallStaticObjectMethodV,
        'CallStaticObjectMethodA': CallStaticObjectMethodA,
        'CallStaticBooleanMethod': CallStaticBooleanMethod,
        'CallStaticBooleanMethodV': CallStaticBooleanMethodV,
        'CallStaticBooleanMethodA': CallStaticBooleanMethodA,
        'CallStaticByteMethod': CallStaticByteMethod,
        'CallStaticByteMethodV': CallStaticByteMethodV,
        'CallStaticByteMethodA': CallStaticByteMethodA,
        'CallStaticCharMethod': CallStaticCharMethod,
        'CallStaticCharMethodV': CallStaticCharMethodV,
        'CallStaticCharMethodA': CallStaticCharMethodA,
        'CallStaticShortMethod': CallStaticShortMethod,
        'CallStaticShortMethodV': CallStaticShortMethodV,
        'CallStaticShortMethodA': CallStaticShortMethodA,
        'CallStaticIntMethod': CallStaticIntMethod,
        'CallStaticIntMethodV': CallStaticIntMethodV,
        'CallStaticIntMethodA': CallStaticIntMethodA,
        'CallStaticLongMethod': CallStaticLongMethod,
        'CallStaticLongMethodV': CallStaticLongMethodV,
        'CallStaticLongMethodA': CallStaticLongMethodA,
        'CallStaticFloatMethod': CallStaticFloatMethod,
        'CallStaticFloatMethodV': CallStaticFloatMethodV,
        'CallStaticFloatMethodA': CallStaticFloatMethodA,
        'CallStaticDoubleMethod': CallStaticDoubleMethod,
        'CallStaticDoubleMethodV': CallStaticDoubleMethodV,
        'CallStaticDoubleMethodA': CallStaticDoubleMethodA,
        'CallStaticVoidMethod': CallStaticVoidMethod,
        'CallStaticVoidMethodV': CallStaticVoidMethodV,
        'CallStaticVoidMethodA': CallStaticVoidMethodA,
        'GetStaticFieldID': GetStaticFieldID,
        'GetStaticObjectField': GetStaticObjectField,
        'GetStaticBooleanField': GetStaticBooleanField,
        'GetStaticByteField': GetStaticByteField,
        'GetStaticCharField': GetStaticCharField,
        'GetStaticShortField': GetStaticShortField,
        'GetStaticIntField': GetStaticIntField,
        'GetStaticLongField': GetStaticLongField,
        'GetStaticFloatField': GetStaticFloatField,
        'GetStaticDoubleField': GetStaticDoubleField,
        'SetStaticObjectField': SetStaticObjectField,
        'SetStaticBooleanField': SetStaticBooleanField,
        'SetStaticByteField': SetStaticByteField,
        'SetStaticCharField': SetStaticCharField,
        'SetStaticShortField': SetStaticShortField,
        'SetStaticIntField': SetStaticIntField,
        'SetStaticLongField': SetStaticLongField,
        'SetStaticFloatField': SetStaticFloatField,
        'SetStaticDoubleField': SetStaticDoubleField,
        'NewString': NewString,
        'GetStringLength': GetStringLength,
        'GetStringChars': GetStringChars,
        'ReleaseStringChars': ReleaseStringChars,
        'NewStringUTF': NewStringUTF,
        'GetStringUTFLength': GetStringUTFLength,
        'GetStringUTFChars': GetStringUTFChars,
        'ReleaseStringUTFChars': ReleaseStringUTFChars,
        'GetArrayLength': GetArrayLength,
        'NewObjectArray': NewObjectArray,
        'GetObjectArrayElement': GetObjectArrayElement,
        'SetObjectArrayElement': SetObjectArrayElement,
        'NewBooleanArray': NewBooleanArray,
        'NewByteArray': NewByteArray,
        'NewCharArray': NewCharArray,
        'NewShortArray': NewShortArray,
        'NewIntArray': NewIntArray,
        'NewLongArray': NewLongArray,
        'NewFloatArray': NewFloatArray,
        'NewDoubleArray': NewDoubleArray,
        'GetBooleanArrayElements': GetBooleanArrayElements,
        'GetByteArrayElements': GetByteArrayElements,
        'GetCharArrayElements': GetCharArrayElements,
        'GetShortArrayElements': GetShortArrayElements,
        'GetIntArrayElements': GetIntArrayElements,
        'GetLongArrayElements': GetLongArrayElements,
        'GetFloatArrayElements': GetFloatArrayElements,
        'GetDoubleArrayElements': GetDoubleArrayElements,
        'ReleaseBooleanArrayElements': ReleaseBooleanArrayElements,
        'ReleaseByteArrayElements': ReleaseByteArrayElements,
        'ReleaseCharArrayElements': ReleaseCharArrayElements,
        'ReleaseShortArrayElements': ReleaseShortArrayElements,
        'ReleaseIntArrayElements': ReleaseIntArrayElements,
        'ReleaseLongArrayElements': ReleaseLongArrayElements,
        'ReleaseFloatArrayElements': ReleaseFloatArrayElements,
        'ReleaseDoubleArrayElements': ReleaseDoubleArrayElements,
        'GetBooleanArrayRegion': GetBooleanArrayRegion,
        'GetByteArrayRegion': GetByteArrayRegion,
        'GetCharArrayRegion': GetCharArrayRegion,
        'GetShortArrayRegion': GetShortArrayRegion,
        'GetIntArrayRegion': GetIntArrayRegion,
        'GetLongArrayRegion': GetLongArrayRegion,
        'GetFloatArrayRegion': GetFloatArrayRegion,
        'GetDoubleArrayRegion': GetDoubleArrayRegion,
        'SetBooleanArrayRegion': SetBooleanArrayRegion,
        'SetByteArrayRegion': SetByteArrayRegion,
        'SetCharArrayRegion': SetCharArrayRegion,
        'SetShortArrayRegion': SetShortArrayRegion,
        'SetIntArrayRegion': SetIntArrayRegion,
        'SetLongArrayRegion': SetLongArrayRegion,
        'SetFloatArrayRegion': SetFloatArrayRegion,
        'SetDoubleArrayRegion': SetDoubleArrayRegion,
        'RegisterNatives': RegisterNatives,
        'UnregisterNatives': UnregisterNatives,
        'MonitorEnter': MonitorEnter,
        'MonitorExit': MonitorExit,
        'GetJavaVM': GetJavaVM,
        'GetStringRegion': GetStringRegion,
        'GetStringUTFRegion': GetStringUTFRegion,
        'GetPrimitiveArrayCritical': GetPrimitiveArrayCritical,
        'ReleasePrimitiveArrayCritical': ReleasePrimitiveArrayCritical,
        'GetStringCritical': GetStringCritical,
        'ReleaseStringCritical': ReleaseStringCritical,
        'NewWeakGlobalRef': NewWeakGlobalRef,
        'DeleteWeakGlobalRef': DeleteWeakGlobalRef,
        'ExceptionCheck': ExceptionCheck,
        'NewDirectByteBuffer': NewDirectByteBuffer,
        'GetDirectBufferAddress': GetDirectBufferAddress,
        'GetDirectBufferCapacity': GetDirectBufferCapacity,
        'GetObjectRefType': GetObjectRefType,
    }

    def __init__(self, project):
        super(JNINativeInterface, self).__init__(project.loader)
        self._provides = 'JNIEnv'
        self._project = project
        self._fptr_size = self._project.arch.bits / 8
        self._project.loader.add_object(self)
        self._construct()
        # Define JNINativeMethod Struct and then resolved in RegisterNatives SimProcedure.
        angr.sim_type.define_struct('struct JNINativeMethod {const char* name;const char* signature;void* fnPtr;}')
        angr.sim_type.parse_type('struct JNINativeMethod')

    def _construct(self):
        # allocate memory for the fake JNINativeInterface struct
        self._JNINativeInterface = self.allocate(
            len(self.JNINativeInterface_index_to_name) * self._fptr_size)
        # allocate memory to JNIEnv (a pointer) and make it to point to the fake JNINativeInterface struct
        self._JNIEnv = self.allocate(self._fptr_size)
        self.memory.write_addr_at(self._JNIEnv - self.min_addr, self._JNINativeInterface)

        # direct calls hook
        for addr in self._project.loader.main_object.symbols_by_addr:
            symb = self._project.loader.main_object.symbols_by_addr[addr]
            if symb.name in self.JNINativeInterface_sig:
                symb_name = symb.name
                jni_native_interface_func_name = self.JNINativeInterface_sig[symb_name]
                if jni_native_interface_func_name in self.JNINativeInterface_name_to_simproc:
                    self._project.hook(addr, self.JNINativeInterface_name_to_simproc[
                        jni_native_interface_func_name]())
                else:
                    self._project.hook(addr, angr.SIM_PROCEDURES['stubs']['ReturnUnconstrained']())

        # iterate through the mapping
        for index, name in self.JNINativeInterface_index_to_name.iteritems():
            # if the mapped value is None (there are 4 reserved entries), hook it with PathTerminator
            if name.startswith('reserved'):
                addr = self.allocate(self._fptr_size)
                self._project.hook(addr, angr.SIM_PROCEDURES['stubs']['PathTerminator']())
            else:
                addr = self.allocate(self._fptr_size)
                # if we have a custom simprocedure for that function, hook with that
                if name in self.JNINativeInterface_name_to_simproc:
                    self._project.hook(addr, self.JNINativeInterface_name_to_simproc[name]())
                # otherwise hook with ReturnUnconstrained
                else:
                    self._project.hook(addr, angr.SIM_PROCEDURES['stubs']['ReturnUnconstrained']())
            self.memory.write_addr_at(self._JNINativeInterface - self.min_addr + index * self._fptr_size, addr)

    @property
    def ptr(self):
        return self._JNIEnv