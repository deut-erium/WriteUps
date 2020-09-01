package com.google.ctf.sandbox;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

/* compiled from: ő */
public class o extends Activity {

    /* renamed from: class  reason: not valid java name */
    long[] f0class = {40999019, 2789358025L, 656272715, 18374979, 3237618335L, 1762529471, 685548119, 382114257, 1436905469, 2126016673, 3318315423L, 797150821};
    int o = 0;

    /* renamed from: o  reason: collision with other field name */
    long[] f1o = new long[12];

    /* access modifiers changed from: protected */
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final EditText editText = (EditText) findViewById(R.id.editText);
        final TextView textView = (TextView) findViewById(R.id.textView);
        ((Button) findViewById(R.id.button)).setOnClickListener(new View.OnClickListener() {
            /*  JADX ERROR: Method load error
                jadx.core.utils.exceptions.DecodeException: Load method exception: Not class type: long in method: com.google.ctf.sandbox.o.1.onClick(android.view.View):void, dex: classes.dex
                	at jadx.core.dex.nodes.MethodNode.load(MethodNode.java:151)
                	at jadx.core.dex.nodes.ClassNode.load(ClassNode.java:286)
                	at jadx.core.dex.nodes.ClassNode.load(ClassNode.java:292)
                	at jadx.core.ProcessClass.process(ProcessClass.java:36)
                	at jadx.core.ProcessClass.generateCode(ProcessClass.java:58)
                	at jadx.core.dex.nodes.ClassNode.decompile(ClassNode.java:273)
                Caused by: jadx.core.utils.exceptions.JadxRuntimeException: Not class type: long
                	at jadx.core.dex.info.ClassInfo.checkClassType(ClassInfo.java:60)
                	at jadx.core.dex.info.ClassInfo.fromType(ClassInfo.java:31)
                	at jadx.core.dex.info.ClassInfo.fromDex(ClassInfo.java:44)
                	at jadx.core.dex.nodes.MethodNode.initTryCatches(MethodNode.java:328)
                	at jadx.core.dex.nodes.MethodNode.load(MethodNode.java:139)
                	... 5 more
                */
            public void onClick(android.view.View r1) {
                /*
                // Can't load method instructions: Load method exception: Not class type: long in method: com.google.ctf.sandbox.o.1.onClick(android.view.View):void, dex: classes.dex
                */
                throw new UnsupportedOperationException("Method not decompiled: com.google.ctf.sandbox.o.AnonymousClass1.onClick(android.view.View):void");
            }
        });
    }
}
