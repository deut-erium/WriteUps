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
            /*  JADX ERROR: JadxRuntimeException in pass: BlockFinish
                jadx.core.utils.exceptions.JadxRuntimeException: Dominance frontier not set for block: B:1:0x0011
                	at jadx.core.dex.nodes.BlockNode.lock(BlockNode.java:75)
                	at jadx.core.utils.ImmutableList.forEach(ImmutableList.java:108)
                	at jadx.core.dex.nodes.MethodNode.finishBasicBlocks(MethodNode.java:472)
                	at jadx.core.dex.visitors.blocksmaker.BlockFinish.visit(BlockFinish.java:27)
                */
            public void onClick(android.view.View r19) {
                /*
                    r18 = this;
                    r1 = r18
                    com.google.ctf.sandbox.o r2 = com.google.ctf.sandbox.o.this
                    r3 = 0
                    r2.o = r3
                    r2 = 49
                    r3 = 0
                    r4 = 3
                    r5 = 2
                    r6 = 1
                    r7 = 4
                    goto L_0x0021
                    r2 = 49
                L_0x0011:
                    r2 = 49
                    r3 = 0
                    r4 = 3
                    r5 = 2
                    r6 = 1
                    r7 = 4
                    goto L_0x0206
                    r2 = 49
                    r3 = 0
                    r4 = 3
                    r5 = 2
                    r6 = 1
                    r7 = 4
                L_0x0021:
                    java.lang.Object[] r2 = new java.lang.Object[r2]
                    r8 = 65
                    java.lang.Integer r8 = java.lang.Integer.valueOf(r8)
                    r2[r3] = r8
                    r8 = 112(0x70, float:1.57E-43)
                    java.lang.Integer r9 = java.lang.Integer.valueOf(r8)
                    r2[r6] = r9
                    java.lang.Integer r8 = java.lang.Integer.valueOf(r8)
                    r2[r5] = r8
                    r8 = 97
                    java.lang.Integer r9 = java.lang.Integer.valueOf(r8)
                    r2[r4] = r9
                    r9 = 114(0x72, float:1.6E-43)
                    java.lang.Integer r9 = java.lang.Integer.valueOf(r9)
                    r2[r7] = r9
                    r9 = 5
                    r10 = 101(0x65, float:1.42E-43)
                    java.lang.Integer r10 = java.lang.Integer.valueOf(r10)
                    r2[r9] = r10
                    r9 = 6
                    r10 = 110(0x6e, float:1.54E-43)
                    java.lang.Integer r11 = java.lang.Integer.valueOf(r10)
                    r2[r9] = r11
                    r9 = 7
                    r11 = 116(0x74, float:1.63E-43)
                    java.lang.Integer r12 = java.lang.Integer.valueOf(r11)
                    r2[r9] = r12
                    r9 = 8
                    r12 = 108(0x6c, float:1.51E-43)
                    java.lang.Integer r12 = java.lang.Integer.valueOf(r12)
                    r2[r9] = r12
                    r9 = 9
                    r12 = 121(0x79, float:1.7E-43)
                    java.lang.Integer r12 = java.lang.Integer.valueOf(r12)
                    r2[r9] = r12
                    r9 = 10
                    r12 = 32
                    java.lang.Integer r13 = java.lang.Integer.valueOf(r12)
                    r2[r9] = r13
                    r9 = 11
                    java.lang.Integer r13 = java.lang.Integer.valueOf(r11)
                    r2[r9] = r13
                    r9 = 12
                    r13 = 104(0x68, float:1.46E-43)
                    java.lang.Integer r14 = java.lang.Integer.valueOf(r13)
                    r2[r9] = r14
                    r9 = 13
                    r14 = 105(0x69, float:1.47E-43)
                    java.lang.Integer r15 = java.lang.Integer.valueOf(r14)
                    r2[r9] = r15
                    r9 = 14
                    r15 = 115(0x73, float:1.61E-43)
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r15)
                    r2[r9] = r16
                    r9 = 15
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r12)
                    r2[r9] = r16
                    r9 = 16
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r14)
                    r2[r9] = r16
                    r9 = 17
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r15)
                    r2[r9] = r16
                    r9 = 18
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r12)
                    r2[r9] = r16
                    r9 = 19
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r10)
                    r2[r9] = r16
                    r9 = 20
                    r3 = 111(0x6f, float:1.56E-43)
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r3)
                    r2[r9] = r16
                    r9 = 21
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r11)
                    r2[r9] = r16
                    r9 = 22
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r12)
                    r2[r9] = r16
                    r9 = 23
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r11)
                    r2[r9] = r16
                    r9 = 24
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r13)
                    r2[r9] = r16
                    r9 = 25
                    r6 = 101(0x65, float:1.42E-43)
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r6)
                    r2[r9] = r6
                    r6 = 26
                    java.lang.Integer r9 = java.lang.Integer.valueOf(r12)
                    r2[r6] = r9
                    r6 = 27
                    r9 = 102(0x66, float:1.43E-43)
                    java.lang.Integer r9 = java.lang.Integer.valueOf(r9)
                    r2[r6] = r9
                    r6 = 28
                    r9 = 108(0x6c, float:1.51E-43)
                    java.lang.Integer r9 = java.lang.Integer.valueOf(r9)
                    r2[r6] = r9
                    r6 = 29
                    java.lang.Integer r9 = java.lang.Integer.valueOf(r8)
                    r2[r6] = r9
                    r6 = 30
                    r9 = 103(0x67, float:1.44E-43)
                    java.lang.Integer r16 = java.lang.Integer.valueOf(r9)
                    r2[r6] = r16
                    r6 = 31
                    r5 = 46
                    java.lang.Integer r5 = java.lang.Integer.valueOf(r5)
                    r2[r6] = r5
                    java.lang.Integer r5 = java.lang.Integer.valueOf(r12)
                    r2[r12] = r5
                    r5 = 33
                    r6 = 87
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r6)
                    r2[r5] = r6
                    r5 = 34
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r13)
                    r2[r5] = r6
                    r5 = 35
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r8)
                    r2[r5] = r6
                    r5 = 36
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r11)
                    r2[r5] = r6
                    r5 = 37
                    r6 = 39
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r6)
                    r2[r5] = r6
                    r5 = 38
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r15)
                    r2[r5] = r6
                    r5 = 39
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r12)
                    r2[r5] = r6
                    r5 = 40
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r9)
                    r2[r5] = r6
                    r5 = 41
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r3)
                    r2[r5] = r6
                    r5 = 42
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r14)
                    r2[r5] = r6
                    r5 = 43
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r10)
                    r2[r5] = r6
                    r5 = 44
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r9)
                    r2[r5] = r6
                    r5 = 45
                    java.lang.Integer r6 = java.lang.Integer.valueOf(r12)
                    r2[r5] = r6
                    r5 = 46
                    java.lang.Integer r3 = java.lang.Integer.valueOf(r3)
                    r2[r5] = r3
                    r3 = 47
                    java.lang.Integer r5 = java.lang.Integer.valueOf(r10)
                    r2[r3] = r5
                    r3 = 48
                    r5 = 63
                    java.lang.Integer r5 = java.lang.Integer.valueOf(r5)
                    r2[r3] = r5
                    java.lang.StringBuilder r3 = new java.lang.StringBuilder
                    r3.<init>()
                    int r5 = r2.length
                    r6 = 0
                L_0x01cf:
                    if (r6 >= r5) goto L_0x01e1
                    r8 = r2[r6]
                    r9 = r8
                    java.lang.Integer r9 = (java.lang.Integer) r9
                    int r9 = r9.intValue()
                    char r9 = (char) r9
                    r3.append(r9)
                    int r6 = r6 + 1
                    goto L_0x01cf
                L_0x01e1:
                    android.widget.EditText r5 = r0
                    android.text.Editable r5 = r5.getText()
                    java.lang.String r5 = r5.toString()
                    java.lang.String r6 = r3.toString()
                    boolean r5 = r5.equals(r6)
                    if (r5 == 0) goto L_0x01fd
                    android.widget.TextView r5 = r1
                    java.lang.String r6 = "🚩"
                    r5.setText(r6)
                    goto L_0x0204
                L_0x01fd:
                    android.widget.TextView r5 = r1
                    java.lang.String r6 = "❌"
                    r5.setText(r6)
                L_0x0204:
                    goto L_0x02c5
                L_0x0206:
                    android.widget.EditText r3 = r0     // Catch:{ Exception -> 0x0011 }
                    android.text.Editable r3 = r3.getText()     // Catch:{ Exception -> 0x0011 }
                    java.lang.String r3 = r3.toString()     // Catch:{ Exception -> 0x0011 }
                    int r5 = r3.length()     // Catch:{ Exception -> 0x0011 }
                    r6 = 48
                    if (r5 == r6) goto L_0x0220
                    android.widget.TextView r4 = r1     // Catch:{ Exception -> 0x0011 }
                    java.lang.String r5 = "❌"
                    r4.setText(r5)     // Catch:{ Exception -> 0x0011 }
                    return
                L_0x0220:
                    r5 = 0
                L_0x0221:
                    int r6 = r3.length()     // Catch:{ Exception -> 0x0011 }
                    int r6 = r6 / r7
                    if (r5 >= r6) goto L_0x0273
                    com.google.ctf.sandbox.o r6 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    long[] r6 = r6.f1o     // Catch:{ Exception -> 0x0011 }
                    int r8 = r5 * 4
                    int r8 = r8 + r4
                    char r8 = r3.charAt(r8)     // Catch:{ Exception -> 0x0011 }
                    int r8 = r8 << 24
                    long r8 = (long) r8     // Catch:{ Exception -> 0x0011 }
                    r6[r5] = r8     // Catch:{ Exception -> 0x0011 }
                    com.google.ctf.sandbox.o r6 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    long[] r6 = r6.f1o     // Catch:{ Exception -> 0x0011 }
                    r8 = r6[r5]     // Catch:{ Exception -> 0x0011 }
                    int r10 = r5 * 4
                    r11 = 2
                    int r10 = r10 + r11
                    char r10 = r3.charAt(r10)     // Catch:{ Exception -> 0x0011 }
                    int r10 = r10 << 16
                    long r12 = (long) r10     // Catch:{ Exception -> 0x0011 }
                    long r8 = r8 | r12
                    r6[r5] = r8     // Catch:{ Exception -> 0x0011 }
                    com.google.ctf.sandbox.o r6 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    long[] r6 = r6.f1o     // Catch:{ Exception -> 0x0011 }
                    r8 = r6[r5]     // Catch:{ Exception -> 0x0011 }
                    int r10 = r5 * 4
                    r12 = 1
                    int r10 = r10 + r12
                    char r10 = r3.charAt(r10)     // Catch:{ Exception -> 0x0011 }
                    int r10 = r10 << 8
                    long r12 = (long) r10     // Catch:{ Exception -> 0x0011 }
                    long r8 = r8 | r12
                    r6[r5] = r8     // Catch:{ Exception -> 0x0011 }
                    com.google.ctf.sandbox.o r6 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    long[] r6 = r6.f1o     // Catch:{ Exception -> 0x0011 }
                    r8 = r6[r5]     // Catch:{ Exception -> 0x0011 }
                    int r10 = r5 * 4
                    char r10 = r3.charAt(r10)     // Catch:{ Exception -> 0x0011 }
                    long r12 = (long) r10     // Catch:{ Exception -> 0x0011 }
                    long r8 = r8 | r12
                    r6[r5] = r8     // Catch:{ Exception -> 0x0011 }
                    int r5 = r5 + 1
                    goto L_0x0221
                L_0x0273:
                    r4 = 4294967296(0x100000000, double:2.121995791E-314)
                    com.google.ctf.sandbox.o r6 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    com.google.ctf.sandbox.o r7 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    long[] r7 = r7.f1o     // Catch:{ Exception -> 0x0011 }
                    com.google.ctf.sandbox.o r8 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    int r8 = r8.o     // Catch:{ Exception -> 0x0011 }
                    r8 = r7[r8]     // Catch:{ Exception -> 0x0011 }
                    long[] r6 = com.google.ctf.sandbox.R.o(r8, r4)     // Catch:{ Exception -> 0x0011 }
                    r7 = 0
                    r7 = r6[r7]     // Catch:{ Exception -> 0x0011 }
                    long r7 = r7 % r4
                    long r7 = r7 + r4
                    long r7 = r7 % r4
                    com.google.ctf.sandbox.o r9 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    long[] r9 = r9.f0class     // Catch:{ Exception -> 0x0011 }
                    com.google.ctf.sandbox.o r10 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    int r10 = r10.o     // Catch:{ Exception -> 0x0011 }
                    r10 = r9[r10]     // Catch:{ Exception -> 0x0011 }
                    int r9 = (r7 > r10 ? 1 : (r7 == r10 ? 0 : -1))
                    if (r9 == 0) goto L_0x02a4
                    android.widget.TextView r9 = r1     // Catch:{ Exception -> 0x0011 }
                    java.lang.String r10 = "❌"
                    r9.setText(r10)     // Catch:{ Exception -> 0x0011 }
                    return
                L_0x02a4:
                    com.google.ctf.sandbox.o r9 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    int r10 = r9.o     // Catch:{ Exception -> 0x0011 }
                    r11 = 1
                    int r10 = r10 + r11
                    r9.o = r10     // Catch:{ Exception -> 0x0011 }
                    com.google.ctf.sandbox.o r9 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    int r9 = r9.o     // Catch:{ Exception -> 0x0011 }
                    com.google.ctf.sandbox.o r10 = com.google.ctf.sandbox.o.this     // Catch:{ Exception -> 0x0011 }
                    long[] r10 = r10.f1o     // Catch:{ Exception -> 0x0011 }
                    int r10 = r10.length     // Catch:{ Exception -> 0x0011 }
                    if (r9 < r10) goto L_0x02bf
                    android.widget.TextView r9 = r1     // Catch:{ Exception -> 0x0011 }
                    java.lang.String r10 = "🚩"
                    r9.setText(r10)     // Catch:{ Exception -> 0x0011 }
                    return
                L_0x02bf:
                    java.lang.RuntimeException r8 = new java.lang.RuntimeException     // Catch:{ Exception -> 0x0011 }
                    r8.<init>()     // Catch:{ Exception -> 0x0011 }
                    throw r8     // Catch:{ Exception -> 0x0011 }
                L_0x02c5:
                    return
                */
                throw new UnsupportedOperationException("Method not decompiled: com.google.ctf.sandbox.o.AnonymousClass1.onClick(android.view.View):void");
            }
        });
    }
}
