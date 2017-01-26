/*
 * Copyright (c) 2017. Fengguo Wei and others.
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution, and is available at
 * http://www.eclipse.org/legal/epl-v10.html
 *
 * Detailed contributors are listed in the CONTRIBUTOR.md
 */

package org.argus.jawa.core

import org.scalatest.{FlatSpec, Matchers}
import org.sireum.util.FileUtil

/**
  * @author <a href="mailto:fgwei521@gmail.com">Fengguo Wei</a>
  */
class ClassHierarchyTest extends FlatSpec with Matchers {

  "Load android.app.Activity" should "resolve android.content.ContextWrapper in Hierarchy" in {
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.getClassOrResolve(new JawaType("android.app.Activity"))
    assert(global.getClassHierarchy.resolved(new JawaType("android.content.ContextWrapper")))
  }

  "Load android.app.Activity" should "let java.lang.Object getAllSubClassesOfIncluding have 5 results" in {
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.getClassOrResolve(new JawaType("android.app.Activity"))
    assert(global.getClassHierarchy.getAllSubClassesOfIncluding(new JawaType("java.lang.Object")).size == 5)
  }

  "Load android.app.Activity" should "let java.lang.Object getAllSubClassesOf have 4 subclasses" in {
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.getClassOrResolve(new JawaType("android.app.Activity"))
    assert(global.getClassHierarchy.getAllSubClassesOf(new JawaType("java.lang.Object")).size == 4)
  }

  "android.app.Activity" should "have 5 superclasses including itself" in {
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.getClassOrResolve(new JawaType("android.app.Activity"))
    assert(global.getClassHierarchy.getAllSuperClassesOfIncluding(new JawaType("android.app.Activity")).size == 5)
  }

  "android.app.Activity" should "have 4 superclasses" in {
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.getClassOrResolve(new JawaType("android.app.Activity"))
    assert(global.getClassHierarchy.getAllSuperClassesOf(new JawaType("android.app.Activity")).size == 4)
  }

  "com.ksu.fieldFlowSentivity.MainActivity" should "have 5 superclasses" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"))
    assert(global.getClassHierarchy.getAllSuperClassesOf(new JawaType("com.ksu.fieldFlowSentivity.MainActivity")).size == 5)
  }

  "Load android.nfc.tech.TagTechnology" should "let java.lang.AutoCloseable get 3 subinterface including itself" in {
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.getClassOrResolve(new JawaType("android.nfc.tech.TagTechnology"))
    assert(global.getClassHierarchy.getAllSubInterfacesOfIncluding(new JawaType("java.lang.AutoCloseable")).size == 3)
  }

  "Load android.nfc.tech.TagTechnology" should "let java.lang.AutoCloseable get 2 subinterface" in {
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.getClassOrResolve(new JawaType("android.nfc.tech.TagTechnology"))
    assert(global.getClassHierarchy.getAllSubInterfacesOf(new JawaType("java.lang.AutoCloseable")).size == 2)
  }

  "Load com.ksu.fieldFlowSentivity.MainActivity and com.ksu.fieldFlowSentivity.FooActivity" should "let android.app.Activity have 3 subclasses including itself" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"))
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.FooActivity"))
    assert(global.getClassHierarchy.getSubClassesOfIncluding(new JawaType("android.app.Activity")).size == 3)
  }

  "Load com.ksu.fieldFlowSentivity.MainActivity and com.ksu.fieldFlowSentivity.FooActivity" should "let android.app.Activity have 2 subclasses" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"))
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.FooActivity"))
    assert(global.getClassHierarchy.getSubClassesOf(new JawaType("android.app.Activity")).size == 2)
  }

  "Load android.nfc.tech.TagTechnology" should "let java.lang.AutoCloseable get subinterface java.io.Closeable" in {
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.getClassOrResolve(new JawaType("android.nfc.tech.TagTechnology"))
    assert(global.getClassHierarchy.getSubInterfacesOfIncluding(new JawaType("java.lang.AutoCloseable")).contains(new JawaType("java.io.Closeable")))
  }

  "Load com.ksu.fieldFlowSentivity.MainActivity" should "let android.view.LayoutInflater$Factory get implementer android.app.Activity" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"))
    assert(global.getClassHierarchy.getAllImplementersOf(new JawaType("android.view.LayoutInflater$Factory")).contains(new JawaType("android.app.Activity")))
  }

  "com.ksu.fieldFlowSentivity.MainActivity" should "recursively subclass of java.lang.Object" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"))
    assert(global.getClassHierarchy.isClassRecursivelySubClassOfIncluding(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"), new JawaType("java.lang.Object")))
  }

  "com.ksu.fieldFlowSentivity.MainActivity" should "be subclass of android.app.Activity" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"))
    assert(global.getClassHierarchy.isClassSubClassOf(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"), new JawaType("android.app.Activity")))
  }

  "java.lang.Object" should "recursively superclass of com.ksu.fieldFlowSentivity.MainActivity" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"))
    assert(global.getClassHierarchy.isClassRecursivelySuperClassOfIncluding(new JawaType("java.lang.Object"), new JawaType("com.ksu.fieldFlowSentivity.MainActivity")))
  }

  "onCreate" should "be visible from com.ksu.fieldFlowSentivity.MainActivity" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"))
    val ms = global.getClassOrResolve(new JawaType("android.app.Activity")).getDeclaredMethodsByName("onCreate")
    assert(ms.forall(m => global.getClassHierarchy.isMethodVisible(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"), m)))
  }

  "com.ksu.fieldFlowSentivity.MainActivity.isDestroyed" should "be dispatched to android.app.Activity.isDestroyed" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    val c: JawaClass = global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.MainActivity"))
    val m: JawaMethod = global.getClassOrResolve(new JawaType("android.app.Activity")).getDeclaredMethodByName("isDestroyed").get
    assert(global.getClassHierarchy.resolveConcreteDispatch(c, m).get.getDeclaringClass.getName == "android.app.Activity")
  }

  "android.app.Activity with process" should "be abstract dispatched to com.ksu.fieldFlowSentivity.FooActivity.process" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    val c: JawaClass = global.getClassOrResolve(new JawaType("android.app.Activity"))
    val m: JawaMethod = global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.FooActivity")).getDeclaredMethodByName("process").get
    assert(global.getClassHierarchy.resolveAbstractDispatch(c, m).exists(m => m.getDeclaringClass.getName == "com.ksu.fieldFlowSentivity.FooActivity"))
  }

  "reset" should "clear all" in {
    val srcUri = FileUtil.toUri(getClass.getResource("/test1").getPath)
    val global = new Global("test", new NoReporter)
    global.setJavaLib(getClass.getResource("/libs/android.jar").getPath)
    global.load(srcUri ,Constants.JAWA_FILE_EXT, DefaultLibraryAPISummary)
    global.getClassOrResolve(new JawaType("android.app.Activity"))
    global.getClassOrResolve(new JawaType("com.ksu.fieldFlowSentivity.FooActivity"))
    global.getClassHierarchy.reset()
    assert(!global.getClassHierarchy.resolved(new JawaType("android.app.Activity")))
  }
}