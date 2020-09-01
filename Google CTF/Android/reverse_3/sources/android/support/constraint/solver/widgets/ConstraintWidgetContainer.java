package android.support.constraint.solver.widgets;

import android.support.constraint.solver.LinearSystem;
import android.support.constraint.solver.Metrics;
import android.support.constraint.solver.widgets.ConstraintAnchor;
import android.support.constraint.solver.widgets.ConstraintWidget;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ConstraintWidgetContainer extends WidgetContainer {
    private static final boolean DEBUG = false;
    static final boolean DEBUG_GRAPH = false;
    private static final boolean DEBUG_LAYOUT = false;
    private static final int MAX_ITERATIONS = 8;
    private static final boolean USE_SNAPSHOT = true;
    int mDebugSolverPassCount = 0;
    public boolean mGroupsWrapOptimized = false;
    private boolean mHeightMeasuredTooSmall = false;
    ChainHead[] mHorizontalChainsArray = new ChainHead[4];
    int mHorizontalChainsSize = 0;
    public boolean mHorizontalWrapOptimized = false;
    private boolean mIsRtl = false;
    private int mOptimizationLevel = 7;
    int mPaddingBottom;
    int mPaddingLeft;
    int mPaddingRight;
    int mPaddingTop;
    public boolean mSkipSolver = false;
    private Snapshot mSnapshot;
    protected LinearSystem mSystem = new LinearSystem();
    ChainHead[] mVerticalChainsArray = new ChainHead[4];
    int mVerticalChainsSize = 0;
    public boolean mVerticalWrapOptimized = false;
    public List<ConstraintWidgetGroup> mWidgetGroups = new ArrayList();
    private boolean mWidthMeasuredTooSmall = false;
    public int mWrapFixedHeight = 0;
    public int mWrapFixedWidth = 0;

    public void fillMetrics(Metrics metrics) {
        this.mSystem.fillMetrics(metrics);
    }

    public ConstraintWidgetContainer() {
    }

    public ConstraintWidgetContainer(int x, int y, int width, int height) {
        super(x, y, width, height);
    }

    public ConstraintWidgetContainer(int width, int height) {
        super(width, height);
    }

    public void setOptimizationLevel(int value) {
        this.mOptimizationLevel = value;
    }

    public int getOptimizationLevel() {
        return this.mOptimizationLevel;
    }

    public boolean optimizeFor(int feature) {
        if ((this.mOptimizationLevel & feature) == feature) {
            return USE_SNAPSHOT;
        }
        return false;
    }

    public String getType() {
        return "ConstraintLayout";
    }

    public void reset() {
        this.mSystem.reset();
        this.mPaddingLeft = 0;
        this.mPaddingRight = 0;
        this.mPaddingTop = 0;
        this.mPaddingBottom = 0;
        this.mWidgetGroups.clear();
        this.mSkipSolver = false;
        super.reset();
    }

    public boolean isWidthMeasuredTooSmall() {
        return this.mWidthMeasuredTooSmall;
    }

    public boolean isHeightMeasuredTooSmall() {
        return this.mHeightMeasuredTooSmall;
    }

    public boolean addChildrenToSolver(LinearSystem system) {
        addToSolver(system);
        int count = this.mChildren.size();
        for (int i = 0; i < count; i++) {
            ConstraintWidget widget = (ConstraintWidget) this.mChildren.get(i);
            if (widget instanceof ConstraintWidgetContainer) {
                ConstraintWidget.DimensionBehaviour horizontalBehaviour = widget.mListDimensionBehaviors[0];
                ConstraintWidget.DimensionBehaviour verticalBehaviour = widget.mListDimensionBehaviors[1];
                if (horizontalBehaviour == ConstraintWidget.DimensionBehaviour.WRAP_CONTENT) {
                    widget.setHorizontalDimensionBehaviour(ConstraintWidget.DimensionBehaviour.FIXED);
                }
                if (verticalBehaviour == ConstraintWidget.DimensionBehaviour.WRAP_CONTENT) {
                    widget.setVerticalDimensionBehaviour(ConstraintWidget.DimensionBehaviour.FIXED);
                }
                widget.addToSolver(system);
                if (horizontalBehaviour == ConstraintWidget.DimensionBehaviour.WRAP_CONTENT) {
                    widget.setHorizontalDimensionBehaviour(horizontalBehaviour);
                }
                if (verticalBehaviour == ConstraintWidget.DimensionBehaviour.WRAP_CONTENT) {
                    widget.setVerticalDimensionBehaviour(verticalBehaviour);
                }
            } else {
                Optimizer.checkMatchParent(this, system, widget);
                widget.addToSolver(system);
            }
        }
        if (this.mHorizontalChainsSize > 0) {
            Chain.applyChainConstraints(this, system, 0);
        }
        if (this.mVerticalChainsSize > 0) {
            Chain.applyChainConstraints(this, system, 1);
        }
        return USE_SNAPSHOT;
    }

    public void updateChildrenFromSolver(LinearSystem system, boolean[] flags) {
        flags[2] = false;
        updateFromSolver(system);
        int count = this.mChildren.size();
        for (int i = 0; i < count; i++) {
            ConstraintWidget widget = (ConstraintWidget) this.mChildren.get(i);
            widget.updateFromSolver(system);
            if (widget.mListDimensionBehaviors[0] == ConstraintWidget.DimensionBehaviour.MATCH_CONSTRAINT && widget.getWidth() < widget.getWrapWidth()) {
                flags[2] = USE_SNAPSHOT;
            }
            if (widget.mListDimensionBehaviors[1] == ConstraintWidget.DimensionBehaviour.MATCH_CONSTRAINT && widget.getHeight() < widget.getWrapHeight()) {
                flags[2] = USE_SNAPSHOT;
            }
        }
    }

    public void setPadding(int left, int top, int right, int bottom) {
        this.mPaddingLeft = left;
        this.mPaddingTop = top;
        this.mPaddingRight = right;
        this.mPaddingBottom = bottom;
    }

    public void setRtl(boolean isRtl) {
        this.mIsRtl = isRtl;
    }

    public boolean isRtl() {
        return this.mIsRtl;
    }

    public void analyze(int optimizationLevel) {
        super.analyze(optimizationLevel);
        int count = this.mChildren.size();
        for (int i = 0; i < count; i++) {
            ((ConstraintWidget) this.mChildren.get(i)).analyze(optimizationLevel);
        }
    }

    /* JADX WARNING: Removed duplicated region for block: B:110:0x0279  */
    /* JADX WARNING: Removed duplicated region for block: B:113:0x0291  */
    /* JADX WARNING: Removed duplicated region for block: B:116:0x02ae  */
    /* JADX WARNING: Removed duplicated region for block: B:118:0x02bd  */
    /* JADX WARNING: Removed duplicated region for block: B:131:0x0307  */
    /* JADX WARNING: Removed duplicated region for block: B:75:0x01a2  */
    /* JADX WARNING: Removed duplicated region for block: B:76:0x01aa  */
    /* JADX WARNING: Removed duplicated region for block: B:95:0x0202  */
    /* Code decompiled incorrectly, please refer to instructions dump. */
    public void layout() {
        /*
            r28 = this;
            r1 = r28
            int r2 = r1.mX
            int r3 = r1.mY
            int r4 = r28.getWidth()
            r5 = 0
            int r4 = java.lang.Math.max(r5, r4)
            int r6 = r28.getHeight()
            int r6 = java.lang.Math.max(r5, r6)
            r1.mWidthMeasuredTooSmall = r5
            r1.mHeightMeasuredTooSmall = r5
            android.support.constraint.solver.widgets.ConstraintWidget r7 = r1.mParent
            if (r7 == 0) goto L_0x0046
            android.support.constraint.solver.widgets.Snapshot r7 = r1.mSnapshot
            if (r7 != 0) goto L_0x002a
            android.support.constraint.solver.widgets.Snapshot r7 = new android.support.constraint.solver.widgets.Snapshot
            r7.<init>(r1)
            r1.mSnapshot = r7
        L_0x002a:
            android.support.constraint.solver.widgets.Snapshot r7 = r1.mSnapshot
            r7.updateFrom(r1)
            int r7 = r1.mPaddingLeft
            r1.setX(r7)
            int r7 = r1.mPaddingTop
            r1.setY(r7)
            r28.resetAnchors()
            android.support.constraint.solver.LinearSystem r7 = r1.mSystem
            android.support.constraint.solver.Cache r7 = r7.getCache()
            r1.resetSolverVariables(r7)
            goto L_0x004a
        L_0x0046:
            r1.mX = r5
            r1.mY = r5
        L_0x004a:
            int r7 = r1.mOptimizationLevel
            r8 = 32
            r9 = 8
            r10 = 1
            if (r7 == 0) goto L_0x006a
            boolean r7 = r1.optimizeFor(r9)
            if (r7 != 0) goto L_0x005c
            r28.optimizeReset()
        L_0x005c:
            boolean r7 = r1.optimizeFor(r8)
            if (r7 != 0) goto L_0x0065
            r28.optimize()
        L_0x0065:
            android.support.constraint.solver.LinearSystem r7 = r1.mSystem
            r7.graphOptimizer = r10
            goto L_0x006e
        L_0x006a:
            android.support.constraint.solver.LinearSystem r7 = r1.mSystem
            r7.graphOptimizer = r5
        L_0x006e:
            r7 = 0
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r11 = r1.mListDimensionBehaviors
            r11 = r11[r10]
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r12 = r1.mListDimensionBehaviors
            r12 = r12[r5]
            r28.resetChains()
            java.util.List<android.support.constraint.solver.widgets.ConstraintWidgetGroup> r13 = r1.mWidgetGroups
            int r13 = r13.size()
            if (r13 != 0) goto L_0x0093
            java.util.List<android.support.constraint.solver.widgets.ConstraintWidgetGroup> r13 = r1.mWidgetGroups
            r13.clear()
            java.util.List<android.support.constraint.solver.widgets.ConstraintWidgetGroup> r13 = r1.mWidgetGroups
            android.support.constraint.solver.widgets.ConstraintWidgetGroup r14 = new android.support.constraint.solver.widgets.ConstraintWidgetGroup
            java.util.ArrayList r15 = r1.mChildren
            r14.<init>(r15)
            r13.add(r5, r14)
        L_0x0093:
            r13 = 0
            java.util.List<android.support.constraint.solver.widgets.ConstraintWidgetGroup> r14 = r1.mWidgetGroups
            int r14 = r14.size()
            java.util.ArrayList r15 = r1.mChildren
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r9 = r28.getHorizontalDimensionBehaviour()
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r10 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            if (r9 == r10) goto L_0x00af
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r9 = r28.getVerticalDimensionBehaviour()
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r10 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            if (r9 != r10) goto L_0x00ad
            goto L_0x00af
        L_0x00ad:
            r9 = r5
            goto L_0x00b0
        L_0x00af:
            r9 = 1
        L_0x00b0:
            r10 = r7
            r7 = r5
        L_0x00b2:
            if (r7 >= r14) goto L_0x0333
            boolean r5 = r1.mSkipSolver
            if (r5 != 0) goto L_0x0333
            java.util.List<android.support.constraint.solver.widgets.ConstraintWidgetGroup> r5 = r1.mWidgetGroups
            java.lang.Object r5 = r5.get(r7)
            android.support.constraint.solver.widgets.ConstraintWidgetGroup r5 = (android.support.constraint.solver.widgets.ConstraintWidgetGroup) r5
            boolean r5 = r5.mSkipSolver
            if (r5 == 0) goto L_0x00cb
            r23 = r3
            r20 = r14
            goto L_0x0328
        L_0x00cb:
            boolean r5 = r1.optimizeFor(r8)
            if (r5 == 0) goto L_0x0100
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r5 = r28.getHorizontalDimensionBehaviour()
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r8 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.FIXED
            if (r5 != r8) goto L_0x00f2
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r5 = r28.getVerticalDimensionBehaviour()
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r8 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.FIXED
            if (r5 != r8) goto L_0x00f2
            java.util.List<android.support.constraint.solver.widgets.ConstraintWidgetGroup> r5 = r1.mWidgetGroups
            java.lang.Object r5 = r5.get(r7)
            android.support.constraint.solver.widgets.ConstraintWidgetGroup r5 = (android.support.constraint.solver.widgets.ConstraintWidgetGroup) r5
            java.util.List r5 = r5.getWidgetsToSolve()
            java.util.ArrayList r5 = (java.util.ArrayList) r5
            r1.mChildren = r5
            goto L_0x0100
        L_0x00f2:
            java.util.List<android.support.constraint.solver.widgets.ConstraintWidgetGroup> r5 = r1.mWidgetGroups
            java.lang.Object r5 = r5.get(r7)
            android.support.constraint.solver.widgets.ConstraintWidgetGroup r5 = (android.support.constraint.solver.widgets.ConstraintWidgetGroup) r5
            java.util.List<android.support.constraint.solver.widgets.ConstraintWidget> r5 = r5.mConstrainedGroup
            java.util.ArrayList r5 = (java.util.ArrayList) r5
            r1.mChildren = r5
        L_0x0100:
            r28.resetChains()
            java.util.ArrayList r5 = r1.mChildren
            int r5 = r5.size()
            r8 = 0
            r13 = 0
        L_0x010b:
            if (r13 >= r5) goto L_0x012a
            r19 = r8
            java.util.ArrayList r8 = r1.mChildren
            java.lang.Object r8 = r8.get(r13)
            android.support.constraint.solver.widgets.ConstraintWidget r8 = (android.support.constraint.solver.widgets.ConstraintWidget) r8
            r20 = r14
            boolean r14 = r8 instanceof android.support.constraint.solver.widgets.WidgetContainer
            if (r14 == 0) goto L_0x0123
            r14 = r8
            android.support.constraint.solver.widgets.WidgetContainer r14 = (android.support.constraint.solver.widgets.WidgetContainer) r14
            r14.layout()
        L_0x0123:
            int r13 = r13 + 1
            r8 = r19
            r14 = r20
            goto L_0x010b
        L_0x012a:
            r19 = r8
            r20 = r14
            r8 = 1
        L_0x012f:
            if (r8 == 0) goto L_0x0313
            int r13 = r19 + 1
            android.support.constraint.solver.LinearSystem r14 = r1.mSystem     // Catch:{ Exception -> 0x017f }
            r14.reset()     // Catch:{ Exception -> 0x017f }
            r28.resetChains()     // Catch:{ Exception -> 0x017f }
            android.support.constraint.solver.LinearSystem r14 = r1.mSystem     // Catch:{ Exception -> 0x017f }
            r1.createObjectVariables(r14)     // Catch:{ Exception -> 0x017f }
            r14 = 0
        L_0x0141:
            if (r14 >= r5) goto L_0x0160
            r21 = r8
            java.util.ArrayList r8 = r1.mChildren     // Catch:{ Exception -> 0x015b }
            java.lang.Object r8 = r8.get(r14)     // Catch:{ Exception -> 0x015b }
            android.support.constraint.solver.widgets.ConstraintWidget r8 = (android.support.constraint.solver.widgets.ConstraintWidget) r8     // Catch:{ Exception -> 0x015b }
            r22 = r10
            android.support.constraint.solver.LinearSystem r10 = r1.mSystem     // Catch:{ Exception -> 0x017c }
            r8.createObjectVariables(r10)     // Catch:{ Exception -> 0x017c }
            int r14 = r14 + 1
            r8 = r21
            r10 = r22
            goto L_0x0141
        L_0x015b:
            r0 = move-exception
            r22 = r10
            r8 = r0
            goto L_0x0185
        L_0x0160:
            r21 = r8
            r22 = r10
            android.support.constraint.solver.LinearSystem r8 = r1.mSystem     // Catch:{ Exception -> 0x017c }
            boolean r8 = r1.addChildrenToSolver(r8)     // Catch:{ Exception -> 0x017c }
            if (r8 == 0) goto L_0x0176
            android.support.constraint.solver.LinearSystem r10 = r1.mSystem     // Catch:{ Exception -> 0x0172 }
            r10.minimize()     // Catch:{ Exception -> 0x0172 }
            goto L_0x0176
        L_0x0172:
            r0 = move-exception
            r21 = r8
            goto L_0x017d
        L_0x0176:
            r23 = r3
            r21 = r8
            goto L_0x01a0
        L_0x017c:
            r0 = move-exception
        L_0x017d:
            r8 = r0
            goto L_0x0185
        L_0x017f:
            r0 = move-exception
            r21 = r8
            r22 = r10
            r8 = r0
        L_0x0185:
            r8.printStackTrace()
            java.io.PrintStream r10 = java.lang.System.out
            java.lang.StringBuilder r14 = new java.lang.StringBuilder
            r14.<init>()
            r23 = r3
            java.lang.String r3 = "EXCEPTION : "
            r14.append(r3)
            r14.append(r8)
            java.lang.String r3 = r14.toString()
            r10.println(r3)
        L_0x01a0:
            if (r21 == 0) goto L_0x01aa
            android.support.constraint.solver.LinearSystem r8 = r1.mSystem
            boolean[] r10 = android.support.constraint.solver.widgets.Optimizer.flags
            r1.updateChildrenFromSolver(r8, r10)
            goto L_0x01f4
        L_0x01aa:
            android.support.constraint.solver.LinearSystem r8 = r1.mSystem
            r1.updateFromSolver(r8)
            r8 = 0
        L_0x01b0:
            if (r8 >= r5) goto L_0x01f4
            java.util.ArrayList r10 = r1.mChildren
            java.lang.Object r10 = r10.get(r8)
            android.support.constraint.solver.widgets.ConstraintWidget r10 = (android.support.constraint.solver.widgets.ConstraintWidget) r10
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r14 = r10.mListDimensionBehaviors
            r18 = 0
            r14 = r14[r18]
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r3 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.MATCH_CONSTRAINT
            if (r14 != r3) goto L_0x01d6
            int r3 = r10.getWidth()
            int r14 = r10.getWrapWidth()
            if (r3 >= r14) goto L_0x01d6
            boolean[] r3 = android.support.constraint.solver.widgets.Optimizer.flags
            r14 = 1
            r17 = 2
            r3[r17] = r14
            goto L_0x01f4
        L_0x01d6:
            r14 = 1
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r3 = r10.mListDimensionBehaviors
            r3 = r3[r14]
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r14 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.MATCH_CONSTRAINT
            if (r3 != r14) goto L_0x01f1
            int r3 = r10.getHeight()
            int r14 = r10.getWrapHeight()
            if (r3 >= r14) goto L_0x01f1
            boolean[] r3 = android.support.constraint.solver.widgets.Optimizer.flags
            r14 = 1
            r17 = 2
            r3[r17] = r14
            goto L_0x01f4
        L_0x01f1:
            int r8 = r8 + 1
            goto L_0x01b0
        L_0x01f4:
            r3 = 0
            if (r9 == 0) goto L_0x0279
            r8 = 8
            if (r13 >= r8) goto L_0x0279
            boolean[] r10 = android.support.constraint.solver.widgets.Optimizer.flags
            r14 = 2
            boolean r10 = r10[r14]
            if (r10 == 0) goto L_0x0279
            r10 = 0
            r14 = 0
            r8 = r14
            r14 = r10
            r10 = 0
        L_0x0207:
            if (r10 >= r5) goto L_0x0234
            r24 = r3
            java.util.ArrayList r3 = r1.mChildren
            java.lang.Object r3 = r3.get(r10)
            android.support.constraint.solver.widgets.ConstraintWidget r3 = (android.support.constraint.solver.widgets.ConstraintWidget) r3
            r25 = r5
            int r5 = r3.mX
            int r16 = r3.getWidth()
            int r5 = r5 + r16
            int r14 = java.lang.Math.max(r14, r5)
            int r5 = r3.mY
            int r16 = r3.getHeight()
            int r5 = r5 + r16
            int r8 = java.lang.Math.max(r8, r5)
            int r10 = r10 + 1
            r3 = r24
            r5 = r25
            goto L_0x0207
        L_0x0234:
            r24 = r3
            r25 = r5
            int r3 = r1.mMinWidth
            int r3 = java.lang.Math.max(r3, r14)
            int r5 = r1.mMinHeight
            int r5 = java.lang.Math.max(r5, r8)
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r8 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            if (r12 != r8) goto L_0x025b
            int r8 = r28.getWidth()
            if (r8 >= r3) goto L_0x025b
            r1.setWidth(r3)
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r8 = r1.mListDimensionBehaviors
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r10 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            r14 = 0
            r8[r14] = r10
            r10 = 1
            r8 = 1
            goto L_0x025f
        L_0x025b:
            r10 = r22
            r8 = r24
        L_0x025f:
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r14 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            if (r11 != r14) goto L_0x0277
            int r14 = r28.getHeight()
            if (r14 >= r5) goto L_0x0277
            r1.setHeight(r5)
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r14 = r1.mListDimensionBehaviors
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r16 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            r17 = 1
            r14[r17] = r16
            r10 = 1
            r3 = 1
            goto L_0x0281
        L_0x0277:
            r3 = r8
            goto L_0x0281
        L_0x0279:
            r24 = r3
            r25 = r5
            r10 = r22
            r3 = r24
        L_0x0281:
            int r5 = r1.mMinWidth
            int r8 = r28.getWidth()
            int r5 = java.lang.Math.max(r5, r8)
            int r8 = r28.getWidth()
            if (r5 <= r8) goto L_0x029e
            r1.setWidth(r5)
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r8 = r1.mListDimensionBehaviors
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r14 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.FIXED
            r16 = 0
            r8[r16] = r14
            r10 = 1
            r3 = 1
        L_0x029e:
            int r8 = r1.mMinHeight
            int r14 = r28.getHeight()
            int r8 = java.lang.Math.max(r8, r14)
            int r14 = r28.getHeight()
            if (r8 <= r14) goto L_0x02bb
            r1.setHeight(r8)
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r14 = r1.mListDimensionBehaviors
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r16 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.FIXED
            r17 = 1
            r14[r17] = r16
            r10 = 1
            r3 = 1
        L_0x02bb:
            if (r10 != 0) goto L_0x0307
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r14 = r1.mListDimensionBehaviors
            r16 = 0
            r14 = r14[r16]
            r26 = r3
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r3 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            if (r14 != r3) goto L_0x02e3
            if (r4 <= 0) goto L_0x02e3
            int r3 = r28.getWidth()
            if (r3 <= r4) goto L_0x02e3
            r3 = 1
            r1.mWidthMeasuredTooSmall = r3
            r10 = 1
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r3 = r1.mListDimensionBehaviors
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r14 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.FIXED
            r16 = 0
            r3[r16] = r14
            r1.setWidth(r4)
            r3 = 1
            r26 = r3
        L_0x02e3:
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r3 = r1.mListDimensionBehaviors
            r14 = 1
            r3 = r3[r14]
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r14 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            if (r3 != r14) goto L_0x0304
            if (r6 <= 0) goto L_0x0304
            int r3 = r28.getHeight()
            if (r3 <= r6) goto L_0x0304
            r3 = 1
            r1.mHeightMeasuredTooSmall = r3
            r10 = 1
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r14 = r1.mListDimensionBehaviors
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r16 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.FIXED
            r14[r3] = r16
            r1.setHeight(r6)
            r3 = 1
            r8 = r3
            goto L_0x030b
        L_0x0304:
            r8 = r26
            goto L_0x030b
        L_0x0307:
            r26 = r3
            r8 = r26
        L_0x030b:
            r19 = r13
            r3 = r23
            r5 = r25
            goto L_0x012f
        L_0x0313:
            r23 = r3
            r25 = r5
            r21 = r8
            r22 = r10
            java.util.List<android.support.constraint.solver.widgets.ConstraintWidgetGroup> r3 = r1.mWidgetGroups
            java.lang.Object r3 = r3.get(r7)
            android.support.constraint.solver.widgets.ConstraintWidgetGroup r3 = (android.support.constraint.solver.widgets.ConstraintWidgetGroup) r3
            r3.updateUnresolvedWidgets()
            r13 = r19
        L_0x0328:
            int r7 = r7 + 1
            r14 = r20
            r3 = r23
            r5 = 0
            r8 = 32
            goto L_0x00b2
        L_0x0333:
            r23 = r3
            r20 = r14
            r3 = r15
            java.util.ArrayList r3 = (java.util.ArrayList) r3
            r1.mChildren = r3
            android.support.constraint.solver.widgets.ConstraintWidget r3 = r1.mParent
            if (r3 == 0) goto L_0x036f
            int r3 = r1.mMinWidth
            int r5 = r28.getWidth()
            int r3 = java.lang.Math.max(r3, r5)
            int r5 = r1.mMinHeight
            int r7 = r28.getHeight()
            int r5 = java.lang.Math.max(r5, r7)
            android.support.constraint.solver.widgets.Snapshot r7 = r1.mSnapshot
            r7.applyTo(r1)
            int r7 = r1.mPaddingLeft
            int r7 = r7 + r3
            int r8 = r1.mPaddingRight
            int r7 = r7 + r8
            r1.setWidth(r7)
            int r7 = r1.mPaddingTop
            int r7 = r7 + r5
            int r8 = r1.mPaddingBottom
            int r7 = r7 + r8
            r1.setHeight(r7)
            r3 = r23
            goto L_0x0375
        L_0x036f:
            r1.mX = r2
            r3 = r23
            r1.mY = r3
        L_0x0375:
            if (r10 == 0) goto L_0x0381
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r5 = r1.mListDimensionBehaviors
            r7 = 0
            r5[r7] = r12
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r5 = r1.mListDimensionBehaviors
            r7 = 1
            r5[r7] = r11
        L_0x0381:
            android.support.constraint.solver.LinearSystem r5 = r1.mSystem
            android.support.constraint.solver.Cache r5 = r5.getCache()
            r1.resetSolverVariables(r5)
            android.support.constraint.solver.widgets.ConstraintWidgetContainer r5 = r28.getRootConstraintContainer()
            if (r1 != r5) goto L_0x0393
            r28.updateDrawPosition()
        L_0x0393:
            return
        */
        throw new UnsupportedOperationException("Method not decompiled: android.support.constraint.solver.widgets.ConstraintWidgetContainer.layout():void");
    }

    public void preOptimize() {
        optimizeReset();
        analyze(this.mOptimizationLevel);
    }

    public void solveGraph() {
        ResolutionAnchor leftNode = getAnchor(ConstraintAnchor.Type.LEFT).getResolutionNode();
        ResolutionAnchor topNode = getAnchor(ConstraintAnchor.Type.TOP).getResolutionNode();
        leftNode.resolve((ResolutionAnchor) null, 0.0f);
        topNode.resolve((ResolutionAnchor) null, 0.0f);
    }

    public void resetGraph() {
        ResolutionAnchor leftNode = getAnchor(ConstraintAnchor.Type.LEFT).getResolutionNode();
        ResolutionAnchor topNode = getAnchor(ConstraintAnchor.Type.TOP).getResolutionNode();
        leftNode.invalidateAnchors();
        topNode.invalidateAnchors();
        leftNode.resolve((ResolutionAnchor) null, 0.0f);
        topNode.resolve((ResolutionAnchor) null, 0.0f);
    }

    public void optimizeForDimensions(int width, int height) {
        if (!(this.mListDimensionBehaviors[0] == ConstraintWidget.DimensionBehaviour.WRAP_CONTENT || this.mResolutionWidth == null)) {
            this.mResolutionWidth.resolve(width);
        }
        if (this.mListDimensionBehaviors[1] != ConstraintWidget.DimensionBehaviour.WRAP_CONTENT && this.mResolutionHeight != null) {
            this.mResolutionHeight.resolve(height);
        }
    }

    public void optimizeReset() {
        int count = this.mChildren.size();
        resetResolutionNodes();
        for (int i = 0; i < count; i++) {
            ((ConstraintWidget) this.mChildren.get(i)).resetResolutionNodes();
        }
    }

    public void optimize() {
        if (!optimizeFor(8)) {
            analyze(this.mOptimizationLevel);
        }
        solveGraph();
    }

    public boolean handlesInternalConstraints() {
        return false;
    }

    public ArrayList<Guideline> getVerticalGuidelines() {
        ArrayList<Guideline> guidelines = new ArrayList<>();
        int mChildrenSize = this.mChildren.size();
        for (int i = 0; i < mChildrenSize; i++) {
            ConstraintWidget widget = (ConstraintWidget) this.mChildren.get(i);
            if (widget instanceof Guideline) {
                Guideline guideline = (Guideline) widget;
                if (guideline.getOrientation() == 1) {
                    guidelines.add(guideline);
                }
            }
        }
        return guidelines;
    }

    public ArrayList<Guideline> getHorizontalGuidelines() {
        ArrayList<Guideline> guidelines = new ArrayList<>();
        int mChildrenSize = this.mChildren.size();
        for (int i = 0; i < mChildrenSize; i++) {
            ConstraintWidget widget = (ConstraintWidget) this.mChildren.get(i);
            if (widget instanceof Guideline) {
                Guideline guideline = (Guideline) widget;
                if (guideline.getOrientation() == 0) {
                    guidelines.add(guideline);
                }
            }
        }
        return guidelines;
    }

    public LinearSystem getSystem() {
        return this.mSystem;
    }

    private void resetChains() {
        this.mHorizontalChainsSize = 0;
        this.mVerticalChainsSize = 0;
    }

    /* access modifiers changed from: package-private */
    public void addChain(ConstraintWidget constraintWidget, int type) {
        ConstraintWidget widget = constraintWidget;
        if (type == 0) {
            addHorizontalChain(widget);
        } else if (type == 1) {
            addVerticalChain(widget);
        }
    }

    private void addHorizontalChain(ConstraintWidget widget) {
        if (this.mHorizontalChainsSize + 1 >= this.mHorizontalChainsArray.length) {
            this.mHorizontalChainsArray = (ChainHead[]) Arrays.copyOf(this.mHorizontalChainsArray, this.mHorizontalChainsArray.length * 2);
        }
        this.mHorizontalChainsArray[this.mHorizontalChainsSize] = new ChainHead(widget, 0, isRtl());
        this.mHorizontalChainsSize++;
    }

    private void addVerticalChain(ConstraintWidget widget) {
        if (this.mVerticalChainsSize + 1 >= this.mVerticalChainsArray.length) {
            this.mVerticalChainsArray = (ChainHead[]) Arrays.copyOf(this.mVerticalChainsArray, this.mVerticalChainsArray.length * 2);
        }
        this.mVerticalChainsArray[this.mVerticalChainsSize] = new ChainHead(widget, 1, isRtl());
        this.mVerticalChainsSize++;
    }

    public List<ConstraintWidgetGroup> getWidgetGroups() {
        return this.mWidgetGroups;
    }
}
