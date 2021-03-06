package com.trolltech.qt.clojure;

import com.trolltech.qt.*;
import com.trolltech.qt.core.QObject;

// Qt expects strongly typed signal fields and slot methods. These classes make it easier to use Qt in clojure.

public class QHolder extends QObject {

  public static interface Arity {
    public Integer arity();
    }

  public static class QSignalHolder0 extends QSignalEmitter {
    public QSignalHolder0() {
      super();
      }
  
    public Signal0 signal;
    
    
    }

  public static class QSignalHolder1 extends QSignalEmitter {
    public QSignalHolder1() {
      super();
      }
  
    public Signal1<Object> signal;
    }
    
  public static class QSignalHolder2 extends QSignalEmitter {
    public QSignalHolder2() {
      super();
      }
  
    public Signal2<Object,Object> signal;
    }
    
  public static class QSignalHolder3 extends QSignalEmitter {
    public QSignalHolder3() {
      super();
      }
  
    public Signal3<Object,Object,Object> signal;
    }
    
  public static class QSignalHolder4 extends QSignalEmitter {
    public QSignalHolder4() {
      super();
      }
  
    public Signal4<Object,Object,Object,Object> signal;
    }
    
  public static class QSignalHolder5 extends QSignalEmitter {
    public QSignalHolder5() {
      super();
      }
  
    public Signal5<Object,Object,Object,Object,Object> signal;
    }
    
  public static class QSignalHolder6 extends QSignalEmitter {
    public QSignalHolder6() {
      super();
      }
  
    public Signal6<Object,Object,Object,Object,Object,Object> signal;
    }
    
  public static class QSignalHolder7 extends QSignalEmitter {
    public QSignalHolder7() {
      super();
      }
  
    public Signal7<Object,Object,Object,Object,Object,Object,Object> signal;
    }
    
  public static class QSignalHolder8 extends QSignalEmitter {
    public QSignalHolder8() {
      super();
      }
  
    public Signal8<Object,Object,Object,Object,Object,Object,Object,Object> signal;
    }
    
  public static class QSignalHolder9 extends QSignalEmitter {
    public QSignalHolder9() {
      super();
      }
  
    public Signal9<Object,Object,Object,Object,Object,Object,Object,Object,Object> signal;
    }
    
  public static class QMethod0 extends QSignalEmitter {
    public QMethod0() {
      super();
      }
    
    public Void method() {
      return null;
      }
    }
    
  public static class QMethod1 extends QSignalEmitter {
    public QMethod1() {
      super();
      }
    
    public Void method(Object o1) {
      return null;
      }
    }
      
  public static class QMethod2 extends QSignalEmitter {
    public QMethod2() {
      super();
      }
    
    public Void method(Object o1, Object o2) {
      return null;
      }
    }
      
  public static class QMethod3 extends QSignalEmitter {
    public QMethod3() {
      super();
      }
    
    public Void method(Object o1, Object o2, Object o3) {
      return null;
      }
    }
      
  public static class QMethod4 extends QSignalEmitter {
    public QMethod4() {
      super();
      }
    
    public Void method(Object o1, Object o2, Object o3, Object o4) {
      return null;
      }
    }
      
  public static class QMethod5 extends QSignalEmitter {
    public QMethod5() {
      super();
      }
    
    public Void method(Object o1, Object o2, Object o3, Object o4, Object o5) {
      return null;
      }
    }
      
  public static class QMethod6 extends QSignalEmitter {
    public QMethod6() {
      super();
      }
    
    public Void method(Object o1, Object o2, Object o3, Object o4, Object o5, Object o6) {
      return null;
      }
    }

  public static class QMethod7 extends QSignalEmitter {
    public QMethod7() {
      super();
      }
    
    public Void method(Object o1, Object o2, Object o3, Object o4, Object o5, Object o6, Object o7) {
      return null;
      }
    }
      
  public static class QMethod8 extends QSignalEmitter {
    public QMethod8() {
      super();
      }
    
    public Void method(Object o1, Object o2, Object o3, Object o4, Object o5, Object o6, Object o7, Object o8) {
      return null;
      }
    }
      
  public static class QMethod9 extends QSignalEmitter {
    public QMethod9() {
      super();
      }
    
    public Void method(Object o1, Object o2, Object o3, Object o4, Object o5, Object o6, Object o7, Object o8, Object o9) {
      return null;
      }
    }
  }