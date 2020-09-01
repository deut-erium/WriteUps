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
            public void onClick(View v) {
                o.this.o = 0;
                String flagString = editText.getText().toString();
                if (flagString.length() != 48) {
                    textView.setText("❌");
                    return;
                }
                for (int i = 0; i < flagString.length() / 4; i++) {
                    o.this.f1o[i] = (long) (flagString.charAt((i * 4) + 3) << 24);
                    long[] jArr = o.this.f1o;
                    jArr[i] = jArr[i] | ((long) (flagString.charAt((i * 4) + 2) << 16));
                    long[] jArr2 = o.this.f1o;
                    jArr2[i] = jArr2[i] | ((long) (flagString.charAt((i * 4) + 1) << 8));
                    long[] jArr3 = o.this.f1o;
                    jArr3[i] = jArr3[i] | ((long) flagString.charAt(i * 4));
                }
                o oVar = o.this;
                if (((R.o(o.this.f1o[o.this.o], 4294967296L)[0] % 4294967296L) + 4294967296L) % 4294967296L != o.this.f0class[o.this.o]) {
                    textView.setText("❌");
                    return;
                }
                o.this.o++;
                if (o.this.o >= o.this.f1o.length) {
                    textView.setText("🚩");
                    return;
                }
                throw new RuntimeException();
            }
        });
    }
}
