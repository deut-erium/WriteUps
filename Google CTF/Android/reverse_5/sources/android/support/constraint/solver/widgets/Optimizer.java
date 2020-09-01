package android.support.constraint.solver.widgets;

import android.support.constraint.solver.LinearSystem;
import android.support.constraint.solver.widgets.ConstraintWidget;

public class Optimizer {
    static final int FLAG_CHAIN_DANGLING = 1;
    static final int FLAG_RECOMPUTE_BOUNDS = 2;
    static final int FLAG_USE_OPTIMIZE = 0;
    public static final int OPTIMIZATION_BARRIER = 2;
    public static final int OPTIMIZATION_CHAIN = 4;
    public static final int OPTIMIZATION_DIMENSIONS = 8;
    public static final int OPTIMIZATION_DIRECT = 1;
    public static final int OPTIMIZATION_GROUPS = 32;
    public static final int OPTIMIZATION_NONE = 0;
    public static final int OPTIMIZATION_RATIO = 16;
    public static final int OPTIMIZATION_STANDARD = 7;
    static boolean[] flags = new boolean[3];

    static void checkMatchParent(ConstraintWidgetContainer container, LinearSystem system, ConstraintWidget widget) {
        if (container.mListDimensionBehaviors[0] != ConstraintWidget.DimensionBehaviour.WRAP_CONTENT && widget.mListDimensionBehaviors[0] == ConstraintWidget.DimensionBehaviour.MATCH_PARENT) {
            int left = widget.mLeft.mMargin;
            int right = container.getWidth() - widget.mRight.mMargin;
            widget.mLeft.mSolverVariable = system.createObjectVariable(widget.mLeft);
            widget.mRight.mSolverVariable = system.createObjectVariable(widget.mRight);
            system.addEquality(widget.mLeft.mSolverVariable, left);
            system.addEquality(widget.mRight.mSolverVariable, right);
            widget.mHorizontalResolution = 2;
            widget.setHorizontalDimension(left, right);
        }
        if (container.mListDimensionBehaviors[1] != ConstraintWidget.DimensionBehaviour.WRAP_CONTENT && widget.mListDimensionBehaviors[1] == ConstraintWidget.DimensionBehaviour.MATCH_PARENT) {
            int top = widget.mTop.mMargin;
            int bottom = container.getHeight() - widget.mBottom.mMargin;
            widget.mTop.mSolverVariable = system.createObjectVariable(widget.mTop);
            widget.mBottom.mSolverVariable = system.createObjectVariable(widget.mBottom);
            system.addEquality(widget.mTop.mSolverVariable, top);
            system.addEquality(widget.mBottom.mSolverVariable, bottom);
            if (widget.mBaselineDistance > 0 || widget.getVisibility() == 8) {
                widget.mBaseline.mSolverVariable = system.createObjectVariable(widget.mBaseline);
                system.addEquality(widget.mBaseline.mSolverVariable, widget.mBaselineDistance + top);
            }
            widget.mVerticalResolution = 2;
            widget.setVerticalDimension(top, bottom);
        }
    }

    /* JADX WARNING: Removed duplicated region for block: B:28:0x003e A[RETURN] */
    /* Code decompiled incorrectly, please refer to instructions dump. */
    private static boolean optimizableMatchConstraint(android.support.constraint.solver.widgets.ConstraintWidget r3, int r4) {
        /*
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r0 = r3.mListDimensionBehaviors
            r0 = r0[r4]
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r1 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.MATCH_CONSTRAINT
            r2 = 0
            if (r0 == r1) goto L_0x000a
            return r2
        L_0x000a:
            float r0 = r3.mDimensionRatio
            r1 = 0
            int r0 = (r0 > r1 ? 1 : (r0 == r1 ? 0 : -1))
            r1 = 1
            if (r0 == 0) goto L_0x0020
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r0 = r3.mListDimensionBehaviors
            if (r4 != 0) goto L_0x0017
            goto L_0x0018
        L_0x0017:
            r1 = r2
        L_0x0018:
            r0 = r0[r1]
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r1 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.MATCH_CONSTRAINT
            if (r0 != r1) goto L_0x001f
            return r2
        L_0x001f:
            return r2
        L_0x0020:
            if (r4 != 0) goto L_0x0030
            int r0 = r3.mMatchConstraintDefaultWidth
            if (r0 == 0) goto L_0x0027
            return r2
        L_0x0027:
            int r0 = r3.mMatchConstraintMinWidth
            if (r0 != 0) goto L_0x002f
            int r0 = r3.mMatchConstraintMaxWidth
            if (r0 == 0) goto L_0x003e
        L_0x002f:
            return r2
        L_0x0030:
            int r0 = r3.mMatchConstraintDefaultHeight
            if (r0 == 0) goto L_0x0035
            return r2
        L_0x0035:
            int r0 = r3.mMatchConstraintMinHeight
            if (r0 != 0) goto L_0x003f
            int r0 = r3.mMatchConstraintMaxHeight
            if (r0 == 0) goto L_0x003e
            goto L_0x003f
        L_0x003e:
            return r1
        L_0x003f:
            return r2
        */
        throw new UnsupportedOperationException("Method not decompiled: android.support.constraint.solver.widgets.Optimizer.optimizableMatchConstraint(android.support.constraint.solver.widgets.ConstraintWidget, int):boolean");
    }

    static void analyze(int optimisationLevel, ConstraintWidget widget) {
        ConstraintWidget constraintWidget = widget;
        widget.updateResolutionNodes();
        ResolutionAnchor leftNode = constraintWidget.mLeft.getResolutionNode();
        ResolutionAnchor topNode = constraintWidget.mTop.getResolutionNode();
        ResolutionAnchor rightNode = constraintWidget.mRight.getResolutionNode();
        ResolutionAnchor bottomNode = constraintWidget.mBottom.getResolutionNode();
        boolean optimiseDimensions = (optimisationLevel & 8) == 8;
        boolean isOptimizableHorizontalMatch = constraintWidget.mListDimensionBehaviors[0] == ConstraintWidget.DimensionBehaviour.MATCH_CONSTRAINT && optimizableMatchConstraint(constraintWidget, 0);
        if (!(leftNode.type == 4 || rightNode.type == 4)) {
            if (constraintWidget.mListDimensionBehaviors[0] == ConstraintWidget.DimensionBehaviour.FIXED || (isOptimizableHorizontalMatch && widget.getVisibility() == 8)) {
                if (constraintWidget.mLeft.mTarget == null && constraintWidget.mRight.mTarget == null) {
                    leftNode.setType(1);
                    rightNode.setType(1);
                    if (optimiseDimensions) {
                        rightNode.dependsOn(leftNode, 1, widget.getResolutionWidth());
                    } else {
                        rightNode.dependsOn(leftNode, widget.getWidth());
                    }
                } else if (constraintWidget.mLeft.mTarget != null && constraintWidget.mRight.mTarget == null) {
                    leftNode.setType(1);
                    rightNode.setType(1);
                    if (optimiseDimensions) {
                        rightNode.dependsOn(leftNode, 1, widget.getResolutionWidth());
                    } else {
                        rightNode.dependsOn(leftNode, widget.getWidth());
                    }
                } else if (constraintWidget.mLeft.mTarget == null && constraintWidget.mRight.mTarget != null) {
                    leftNode.setType(1);
                    rightNode.setType(1);
                    leftNode.dependsOn(rightNode, -widget.getWidth());
                    if (optimiseDimensions) {
                        leftNode.dependsOn(rightNode, -1, widget.getResolutionWidth());
                    } else {
                        leftNode.dependsOn(rightNode, -widget.getWidth());
                    }
                } else if (!(constraintWidget.mLeft.mTarget == null || constraintWidget.mRight.mTarget == null)) {
                    leftNode.setType(2);
                    rightNode.setType(2);
                    if (optimiseDimensions) {
                        widget.getResolutionWidth().addDependent(leftNode);
                        widget.getResolutionWidth().addDependent(rightNode);
                        leftNode.setOpposite(rightNode, -1, widget.getResolutionWidth());
                        rightNode.setOpposite(leftNode, 1, widget.getResolutionWidth());
                    } else {
                        leftNode.setOpposite(rightNode, (float) (-widget.getWidth()));
                        rightNode.setOpposite(leftNode, (float) widget.getWidth());
                    }
                }
            } else if (isOptimizableHorizontalMatch) {
                int width = widget.getWidth();
                leftNode.setType(1);
                rightNode.setType(1);
                if (constraintWidget.mLeft.mTarget == null && constraintWidget.mRight.mTarget == null) {
                    if (optimiseDimensions) {
                        rightNode.dependsOn(leftNode, 1, widget.getResolutionWidth());
                    } else {
                        rightNode.dependsOn(leftNode, width);
                    }
                } else if (constraintWidget.mLeft.mTarget == null || constraintWidget.mRight.mTarget != null) {
                    if (constraintWidget.mLeft.mTarget != null || constraintWidget.mRight.mTarget == null) {
                        if (!(constraintWidget.mLeft.mTarget == null || constraintWidget.mRight.mTarget == null)) {
                            if (optimiseDimensions) {
                                widget.getResolutionWidth().addDependent(leftNode);
                                widget.getResolutionWidth().addDependent(rightNode);
                            }
                            if (constraintWidget.mDimensionRatio == 0.0f) {
                                leftNode.setType(3);
                                rightNode.setType(3);
                                leftNode.setOpposite(rightNode, 0.0f);
                                rightNode.setOpposite(leftNode, 0.0f);
                            } else {
                                leftNode.setType(2);
                                rightNode.setType(2);
                                leftNode.setOpposite(rightNode, (float) (-width));
                                rightNode.setOpposite(leftNode, (float) width);
                                constraintWidget.setWidth(width);
                            }
                        }
                    } else if (optimiseDimensions) {
                        leftNode.dependsOn(rightNode, -1, widget.getResolutionWidth());
                    } else {
                        leftNode.dependsOn(rightNode, -width);
                    }
                } else if (optimiseDimensions) {
                    rightNode.dependsOn(leftNode, 1, widget.getResolutionWidth());
                } else {
                    rightNode.dependsOn(leftNode, width);
                }
            }
        }
        boolean isOptimizableVerticalMatch = constraintWidget.mListDimensionBehaviors[1] == ConstraintWidget.DimensionBehaviour.MATCH_CONSTRAINT && optimizableMatchConstraint(constraintWidget, 1);
        if (topNode.type != 4 && bottomNode.type != 4) {
            if (constraintWidget.mListDimensionBehaviors[1] == ConstraintWidget.DimensionBehaviour.FIXED || (isOptimizableVerticalMatch && widget.getVisibility() == 8)) {
                if (constraintWidget.mTop.mTarget == null && constraintWidget.mBottom.mTarget == null) {
                    topNode.setType(1);
                    bottomNode.setType(1);
                    if (optimiseDimensions) {
                        bottomNode.dependsOn(topNode, 1, widget.getResolutionHeight());
                    } else {
                        bottomNode.dependsOn(topNode, widget.getHeight());
                    }
                    if (constraintWidget.mBaseline.mTarget != null) {
                        constraintWidget.mBaseline.getResolutionNode().setType(1);
                        topNode.dependsOn(1, constraintWidget.mBaseline.getResolutionNode(), -constraintWidget.mBaselineDistance);
                    }
                } else if (constraintWidget.mTop.mTarget != null && constraintWidget.mBottom.mTarget == null) {
                    topNode.setType(1);
                    bottomNode.setType(1);
                    if (optimiseDimensions) {
                        bottomNode.dependsOn(topNode, 1, widget.getResolutionHeight());
                    } else {
                        bottomNode.dependsOn(topNode, widget.getHeight());
                    }
                    if (constraintWidget.mBaselineDistance > 0) {
                        constraintWidget.mBaseline.getResolutionNode().dependsOn(1, topNode, constraintWidget.mBaselineDistance);
                    }
                } else if (constraintWidget.mTop.mTarget == null && constraintWidget.mBottom.mTarget != null) {
                    topNode.setType(1);
                    bottomNode.setType(1);
                    if (optimiseDimensions) {
                        topNode.dependsOn(bottomNode, -1, widget.getResolutionHeight());
                    } else {
                        topNode.dependsOn(bottomNode, -widget.getHeight());
                    }
                    if (constraintWidget.mBaselineDistance > 0) {
                        constraintWidget.mBaseline.getResolutionNode().dependsOn(1, topNode, constraintWidget.mBaselineDistance);
                    }
                } else if (constraintWidget.mTop.mTarget != null && constraintWidget.mBottom.mTarget != null) {
                    topNode.setType(2);
                    bottomNode.setType(2);
                    if (optimiseDimensions) {
                        topNode.setOpposite(bottomNode, -1, widget.getResolutionHeight());
                        bottomNode.setOpposite(topNode, 1, widget.getResolutionHeight());
                        widget.getResolutionHeight().addDependent(topNode);
                        widget.getResolutionWidth().addDependent(bottomNode);
                    } else {
                        topNode.setOpposite(bottomNode, (float) (-widget.getHeight()));
                        bottomNode.setOpposite(topNode, (float) widget.getHeight());
                    }
                    if (constraintWidget.mBaselineDistance > 0) {
                        constraintWidget.mBaseline.getResolutionNode().dependsOn(1, topNode, constraintWidget.mBaselineDistance);
                    }
                }
            } else if (isOptimizableVerticalMatch) {
                int height = widget.getHeight();
                topNode.setType(1);
                bottomNode.setType(1);
                if (constraintWidget.mTop.mTarget == null && constraintWidget.mBottom.mTarget == null) {
                    if (optimiseDimensions) {
                        bottomNode.dependsOn(topNode, 1, widget.getResolutionHeight());
                    } else {
                        bottomNode.dependsOn(topNode, height);
                    }
                } else if (constraintWidget.mTop.mTarget == null || constraintWidget.mBottom.mTarget != null) {
                    if (constraintWidget.mTop.mTarget != null || constraintWidget.mBottom.mTarget == null) {
                        if (constraintWidget.mTop.mTarget != null && constraintWidget.mBottom.mTarget != null) {
                            if (optimiseDimensions) {
                                widget.getResolutionHeight().addDependent(topNode);
                                widget.getResolutionWidth().addDependent(bottomNode);
                            }
                            if (constraintWidget.mDimensionRatio == 0.0f) {
                                topNode.setType(3);
                                bottomNode.setType(3);
                                topNode.setOpposite(bottomNode, 0.0f);
                                bottomNode.setOpposite(topNode, 0.0f);
                                return;
                            }
                            topNode.setType(2);
                            bottomNode.setType(2);
                            topNode.setOpposite(bottomNode, (float) (-height));
                            bottomNode.setOpposite(topNode, (float) height);
                            constraintWidget.setHeight(height);
                            if (constraintWidget.mBaselineDistance > 0) {
                                constraintWidget.mBaseline.getResolutionNode().dependsOn(1, topNode, constraintWidget.mBaselineDistance);
                            }
                        }
                    } else if (optimiseDimensions) {
                        topNode.dependsOn(bottomNode, -1, widget.getResolutionHeight());
                    } else {
                        topNode.dependsOn(bottomNode, -height);
                    }
                } else if (optimiseDimensions) {
                    bottomNode.dependsOn(topNode, 1, widget.getResolutionHeight());
                } else {
                    bottomNode.dependsOn(topNode, height);
                }
            }
        }
    }

    /* JADX WARNING: Removed duplicated region for block: B:81:0x013b  */
    /* JADX WARNING: Removed duplicated region for block: B:82:0x0141  */
    /* Code decompiled incorrectly, please refer to instructions dump. */
    static boolean applyChainOptimized(android.support.constraint.solver.widgets.ConstraintWidgetContainer r43, android.support.constraint.solver.LinearSystem r44, int r45, int r46, android.support.constraint.solver.widgets.ChainHead r47) {
        /*
            r0 = r44
            r1 = r45
            r2 = r47
            android.support.constraint.solver.widgets.ConstraintWidget r3 = r2.mFirst
            android.support.constraint.solver.widgets.ConstraintWidget r4 = r2.mLast
            android.support.constraint.solver.widgets.ConstraintWidget r5 = r2.mFirstVisibleWidget
            android.support.constraint.solver.widgets.ConstraintWidget r6 = r2.mLastVisibleWidget
            android.support.constraint.solver.widgets.ConstraintWidget r7 = r2.mHead
            r8 = r3
            r9 = 0
            r10 = 0
            r11 = 0
            float r12 = r2.mTotalWeight
            android.support.constraint.solver.widgets.ConstraintWidget r13 = r2.mFirstMatchConstraintWidget
            android.support.constraint.solver.widgets.ConstraintWidget r14 = r2.mLastMatchConstraintWidget
            r2 = r43
            r15 = r8
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r8 = r2.mListDimensionBehaviors
            r8 = r8[r1]
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r2 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            r16 = 0
            r17 = r9
            if (r8 != r2) goto L_0x002b
            r2 = 1
            goto L_0x002d
        L_0x002b:
            r2 = r16
        L_0x002d:
            r8 = 0
            r18 = 0
            r19 = 0
            if (r1 != 0) goto L_0x0054
            int r9 = r7.mHorizontalChainStyle
            if (r9 != 0) goto L_0x003a
            r9 = 1
            goto L_0x003c
        L_0x003a:
            r9 = r16
        L_0x003c:
            r8 = r9
            int r9 = r7.mHorizontalChainStyle
            r21 = r2
            r2 = 1
            if (r9 != r2) goto L_0x0046
            r2 = 1
            goto L_0x0048
        L_0x0046:
            r2 = r16
        L_0x0048:
            int r9 = r7.mHorizontalChainStyle
            r22 = r2
            r2 = 2
            if (r9 != r2) goto L_0x0051
            r2 = 1
            goto L_0x0053
        L_0x0051:
            r2 = r16
        L_0x0053:
            goto L_0x0075
        L_0x0054:
            r21 = r2
            int r2 = r7.mVerticalChainStyle
            if (r2 != 0) goto L_0x005c
            r2 = 1
            goto L_0x005e
        L_0x005c:
            r2 = r16
        L_0x005e:
            r8 = r2
            int r2 = r7.mVerticalChainStyle
            r9 = 1
            if (r2 != r9) goto L_0x0066
            r2 = 1
            goto L_0x0068
        L_0x0066:
            r2 = r16
        L_0x0068:
            int r9 = r7.mVerticalChainStyle
            r23 = r2
            r2 = 2
            if (r9 != r2) goto L_0x0071
            r2 = 1
            goto L_0x0073
        L_0x0071:
            r2 = r16
        L_0x0073:
            r22 = r23
        L_0x0075:
            r9 = 0
            r18 = 0
            r24 = r7
            r7 = r11
            r11 = r15
            r15 = r9
            r9 = r16
        L_0x007f:
            r19 = 0
            r25 = r13
            r13 = 8
            if (r10 != 0) goto L_0x014b
            r26 = r10
            int r10 = r11.getVisibility()
            if (r10 == r13) goto L_0x00d2
            int r9 = r9 + 1
            if (r1 != 0) goto L_0x009a
            int r10 = r11.getWidth()
            float r10 = (float) r10
            float r15 = r15 + r10
            goto L_0x00a0
        L_0x009a:
            int r10 = r11.getHeight()
            float r10 = (float) r10
            float r15 = r15 + r10
        L_0x00a0:
            if (r11 == r5) goto L_0x00ac
            android.support.constraint.solver.widgets.ConstraintAnchor[] r10 = r11.mListAnchors
            r10 = r10[r46]
            int r10 = r10.getMargin()
            float r10 = (float) r10
            float r15 = r15 + r10
        L_0x00ac:
            if (r11 == r6) goto L_0x00ba
            android.support.constraint.solver.widgets.ConstraintAnchor[] r10 = r11.mListAnchors
            int r20 = r46 + 1
            r10 = r10[r20]
            int r10 = r10.getMargin()
            float r10 = (float) r10
            float r15 = r15 + r10
        L_0x00ba:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r10 = r11.mListAnchors
            r10 = r10[r46]
            int r10 = r10.getMargin()
            float r10 = (float) r10
            float r18 = r18 + r10
            android.support.constraint.solver.widgets.ConstraintAnchor[] r10 = r11.mListAnchors
            int r20 = r46 + 1
            r10 = r10[r20]
            int r10 = r10.getMargin()
            float r10 = (float) r10
            float r18 = r18 + r10
        L_0x00d2:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r10 = r11.mListAnchors
            r10 = r10[r46]
            r27 = r9
            int r9 = r11.getVisibility()
            if (r9 == r13) goto L_0x010e
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r9 = r11.mListDimensionBehaviors
            r9 = r9[r1]
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r13 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.MATCH_CONSTRAINT
            if (r9 != r13) goto L_0x010e
            int r7 = r7 + 1
            if (r1 != 0) goto L_0x00f8
            int r9 = r11.mMatchConstraintDefaultWidth
            if (r9 == 0) goto L_0x00ef
            return r16
        L_0x00ef:
            int r9 = r11.mMatchConstraintMinWidth
            if (r9 != 0) goto L_0x00f7
            int r9 = r11.mMatchConstraintMaxWidth
            if (r9 == 0) goto L_0x0106
        L_0x00f7:
            return r16
        L_0x00f8:
            int r9 = r11.mMatchConstraintDefaultHeight
            if (r9 == 0) goto L_0x00fd
            return r16
        L_0x00fd:
            int r9 = r11.mMatchConstraintMinHeight
            if (r9 != 0) goto L_0x010d
            int r9 = r11.mMatchConstraintMaxHeight
            if (r9 == 0) goto L_0x0106
            goto L_0x010d
        L_0x0106:
            float r9 = r11.mDimensionRatio
            int r9 = (r9 > r19 ? 1 : (r9 == r19 ? 0 : -1))
            if (r9 == 0) goto L_0x010e
            return r16
        L_0x010d:
            return r16
        L_0x010e:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r9 = r11.mListAnchors
            int r13 = r46 + 1
            r9 = r9[r13]
            android.support.constraint.solver.widgets.ConstraintAnchor r9 = r9.mTarget
            if (r9 == 0) goto L_0x0134
            android.support.constraint.solver.widgets.ConstraintWidget r13 = r9.mOwner
            r28 = r7
            android.support.constraint.solver.widgets.ConstraintAnchor[] r7 = r13.mListAnchors
            r7 = r7[r46]
            android.support.constraint.solver.widgets.ConstraintAnchor r7 = r7.mTarget
            if (r7 == 0) goto L_0x0132
            android.support.constraint.solver.widgets.ConstraintAnchor[] r7 = r13.mListAnchors
            r7 = r7[r46]
            android.support.constraint.solver.widgets.ConstraintAnchor r7 = r7.mTarget
            android.support.constraint.solver.widgets.ConstraintWidget r7 = r7.mOwner
            if (r7 == r11) goto L_0x012f
            goto L_0x0132
        L_0x012f:
            r17 = r13
            goto L_0x0139
        L_0x0132:
            r7 = 0
            goto L_0x0137
        L_0x0134:
            r28 = r7
            r7 = 0
        L_0x0137:
            r17 = r7
        L_0x0139:
            if (r17 == 0) goto L_0x0141
            r7 = r17
            r11 = r7
            r10 = r26
            goto L_0x0143
        L_0x0141:
            r7 = 1
            r10 = r7
        L_0x0143:
            r13 = r25
            r9 = r27
            r7 = r28
            goto L_0x007f
        L_0x014b:
            r26 = r10
            android.support.constraint.solver.widgets.ConstraintAnchor[] r10 = r3.mListAnchors
            r10 = r10[r46]
            android.support.constraint.solver.widgets.ResolutionAnchor r10 = r10.getResolutionNode()
            android.support.constraint.solver.widgets.ConstraintAnchor[] r13 = r4.mListAnchors
            int r20 = r46 + 1
            r13 = r13[r20]
            android.support.constraint.solver.widgets.ResolutionAnchor r13 = r13.getResolutionNode()
            r29 = r14
            android.support.constraint.solver.widgets.ResolutionAnchor r14 = r10.target
            if (r14 == 0) goto L_0x04ba
            android.support.constraint.solver.widgets.ResolutionAnchor r14 = r13.target
            if (r14 != 0) goto L_0x0179
            r30 = r2
            r32 = r6
            r39 = r7
            r33 = r8
            r40 = r9
            r35 = r13
            r13 = r0
            r9 = r3
            goto L_0x04c8
        L_0x0179:
            android.support.constraint.solver.widgets.ResolutionAnchor r14 = r10.target
            int r14 = r14.state
            r0 = 1
            if (r14 != r0) goto L_0x04aa
            android.support.constraint.solver.widgets.ResolutionAnchor r14 = r13.target
            int r14 = r14.state
            if (r14 == r0) goto L_0x0197
            r30 = r2
            r32 = r6
            r39 = r7
            r33 = r8
            r40 = r9
            r35 = r13
            r13 = r44
            r9 = r3
            goto L_0x04b9
        L_0x0197:
            if (r7 <= 0) goto L_0x019c
            if (r7 == r9) goto L_0x019c
            return r16
        L_0x019c:
            r0 = 0
            if (r2 != 0) goto L_0x01a3
            if (r8 != 0) goto L_0x01a3
            if (r22 == 0) goto L_0x01bc
        L_0x01a3:
            if (r5 == 0) goto L_0x01ae
            android.support.constraint.solver.widgets.ConstraintAnchor[] r14 = r5.mListAnchors
            r14 = r14[r46]
            int r14 = r14.getMargin()
            float r0 = (float) r14
        L_0x01ae:
            if (r6 == 0) goto L_0x01bc
            android.support.constraint.solver.widgets.ConstraintAnchor[] r14 = r6.mListAnchors
            int r20 = r46 + 1
            r14 = r14[r20]
            int r14 = r14.getMargin()
            float r14 = (float) r14
            float r0 = r0 + r14
        L_0x01bc:
            android.support.constraint.solver.widgets.ResolutionAnchor r14 = r10.target
            float r14 = r14.resolvedOffset
            r30 = r2
            android.support.constraint.solver.widgets.ResolutionAnchor r2 = r13.target
            float r2 = r2.resolvedOffset
            r20 = 0
            int r23 = (r14 > r2 ? 1 : (r14 == r2 ? 0 : -1))
            if (r23 >= 0) goto L_0x01d1
            float r23 = r2 - r14
            float r23 = r23 - r15
        L_0x01d0:
            goto L_0x01d6
        L_0x01d1:
            float r23 = r14 - r2
            float r23 = r23 - r15
            goto L_0x01d0
        L_0x01d6:
            r27 = 1
            if (r7 <= 0) goto L_0x02c4
            if (r7 != r9) goto L_0x02c4
            android.support.constraint.solver.widgets.ConstraintWidget r20 = r11.getParent()
            if (r20 == 0) goto L_0x01f3
            r31 = r2
            android.support.constraint.solver.widgets.ConstraintWidget r2 = r11.getParent()
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r2 = r2.mListDimensionBehaviors
            r2 = r2[r1]
            r32 = r6
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r6 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            if (r2 != r6) goto L_0x01f7
            return r16
        L_0x01f3:
            r31 = r2
            r32 = r6
        L_0x01f7:
            float r23 = r23 + r15
            float r23 = r23 - r18
            r2 = r3
            r6 = r2
            r2 = r14
        L_0x01fe:
            if (r6 == 0) goto L_0x02b8
            android.support.constraint.solver.Metrics r11 = android.support.constraint.solver.LinearSystem.sMetrics
            if (r11 == 0) goto L_0x0225
            android.support.constraint.solver.Metrics r11 = android.support.constraint.solver.LinearSystem.sMetrics
            r33 = r8
            r34 = r9
            long r8 = r11.nonresolvedWidgets
            long r8 = r8 - r27
            r11.nonresolvedWidgets = r8
            android.support.constraint.solver.Metrics r8 = android.support.constraint.solver.LinearSystem.sMetrics
            r35 = r13
            r36 = r14
            long r13 = r8.resolvedWidgets
            long r13 = r13 + r27
            r8.resolvedWidgets = r13
            android.support.constraint.solver.Metrics r8 = android.support.constraint.solver.LinearSystem.sMetrics
            long r13 = r8.chainConnectionResolved
            long r13 = r13 + r27
            r8.chainConnectionResolved = r13
            goto L_0x022d
        L_0x0225:
            r33 = r8
            r34 = r9
            r35 = r13
            r36 = r14
        L_0x022d:
            android.support.constraint.solver.widgets.ConstraintWidget[] r8 = r6.mNextChainWidget
            r17 = r8[r1]
            if (r17 != 0) goto L_0x0239
            if (r6 != r4) goto L_0x0236
            goto L_0x0239
        L_0x0236:
            r13 = r44
            goto L_0x02ac
        L_0x0239:
            float r8 = (float) r7
            float r8 = r23 / r8
            int r9 = (r12 > r19 ? 1 : (r12 == r19 ? 0 : -1))
            if (r9 <= 0) goto L_0x0254
            float[] r9 = r6.mWeight
            r9 = r9[r1]
            r11 = -1082130432(0xffffffffbf800000, float:-1.0)
            int r9 = (r9 > r11 ? 1 : (r9 == r11 ? 0 : -1))
            if (r9 != 0) goto L_0x024c
            r8 = 0
            goto L_0x0254
        L_0x024c:
            float[] r9 = r6.mWeight
            r9 = r9[r1]
            float r9 = r9 * r23
            float r8 = r9 / r12
        L_0x0254:
            int r9 = r6.getVisibility()
            r11 = 8
            if (r9 != r11) goto L_0x025d
            r8 = 0
        L_0x025d:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r9 = r6.mListAnchors
            r9 = r9[r46]
            int r9 = r9.getMargin()
            float r9 = (float) r9
            float r2 = r2 + r9
            android.support.constraint.solver.widgets.ConstraintAnchor[] r9 = r6.mListAnchors
            r9 = r9[r46]
            android.support.constraint.solver.widgets.ResolutionAnchor r9 = r9.getResolutionNode()
            android.support.constraint.solver.widgets.ResolutionAnchor r11 = r10.resolvedTarget
            r9.resolve(r11, r2)
            android.support.constraint.solver.widgets.ConstraintAnchor[] r9 = r6.mListAnchors
            int r11 = r46 + 1
            r9 = r9[r11]
            android.support.constraint.solver.widgets.ResolutionAnchor r9 = r9.getResolutionNode()
            android.support.constraint.solver.widgets.ResolutionAnchor r11 = r10.resolvedTarget
            float r13 = r2 + r8
            r9.resolve(r11, r13)
            android.support.constraint.solver.widgets.ConstraintAnchor[] r9 = r6.mListAnchors
            r9 = r9[r46]
            android.support.constraint.solver.widgets.ResolutionAnchor r9 = r9.getResolutionNode()
            r13 = r44
            r9.addResolvedValue(r13)
            android.support.constraint.solver.widgets.ConstraintAnchor[] r9 = r6.mListAnchors
            int r11 = r46 + 1
            r9 = r9[r11]
            android.support.constraint.solver.widgets.ResolutionAnchor r9 = r9.getResolutionNode()
            r9.addResolvedValue(r13)
            float r2 = r2 + r8
            android.support.constraint.solver.widgets.ConstraintAnchor[] r9 = r6.mListAnchors
            int r11 = r46 + 1
            r9 = r9[r11]
            int r9 = r9.getMargin()
            float r9 = (float) r9
            float r2 = r2 + r9
        L_0x02ac:
            r6 = r17
            r8 = r33
            r9 = r34
            r13 = r35
            r14 = r36
            goto L_0x01fe
        L_0x02b8:
            r33 = r8
            r34 = r9
            r35 = r13
            r36 = r14
            r13 = r44
            r8 = 1
            return r8
        L_0x02c4:
            r31 = r2
            r32 = r6
            r33 = r8
            r34 = r9
            r35 = r13
            r36 = r14
            r13 = r44
            int r2 = (r23 > r19 ? 1 : (r23 == r19 ? 0 : -1))
            if (r2 >= 0) goto L_0x02db
            r8 = 0
            r22 = 0
            r2 = 1
            goto L_0x02df
        L_0x02db:
            r2 = r30
            r8 = r33
        L_0x02df:
            if (r2 == 0) goto L_0x0394
            float r23 = r23 - r0
            r6 = r3
            float r9 = r3.getBiasPercent(r1)
            float r9 = r9 * r23
            float r14 = r36 + r9
            r11 = r6
            r23 = r14
        L_0x02ef:
            if (r11 == 0) goto L_0x0389
            android.support.constraint.solver.Metrics r6 = android.support.constraint.solver.LinearSystem.sMetrics
            if (r6 == 0) goto L_0x0314
            android.support.constraint.solver.Metrics r6 = android.support.constraint.solver.LinearSystem.sMetrics
            r38 = r2
            r37 = r3
            long r2 = r6.nonresolvedWidgets
            long r2 = r2 - r27
            r6.nonresolvedWidgets = r2
            android.support.constraint.solver.Metrics r2 = android.support.constraint.solver.LinearSystem.sMetrics
            r39 = r7
            long r6 = r2.resolvedWidgets
            long r6 = r6 + r27
            r2.resolvedWidgets = r6
            android.support.constraint.solver.Metrics r2 = android.support.constraint.solver.LinearSystem.sMetrics
            long r6 = r2.chainConnectionResolved
            long r6 = r6 + r27
            r2.chainConnectionResolved = r6
            goto L_0x031a
        L_0x0314:
            r38 = r2
            r37 = r3
            r39 = r7
        L_0x031a:
            android.support.constraint.solver.widgets.ConstraintWidget[] r2 = r11.mNextChainWidget
            r17 = r2[r1]
            if (r17 != 0) goto L_0x0322
            if (r11 != r4) goto L_0x037f
        L_0x0322:
            r2 = 0
            if (r1 != 0) goto L_0x032b
            int r3 = r11.getWidth()
            float r2 = (float) r3
            goto L_0x0330
        L_0x032b:
            int r3 = r11.getHeight()
            float r2 = (float) r3
        L_0x0330:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r11.mListAnchors
            r3 = r3[r46]
            int r3 = r3.getMargin()
            float r3 = (float) r3
            float r3 = r23 + r3
            android.support.constraint.solver.widgets.ConstraintAnchor[] r6 = r11.mListAnchors
            r6 = r6[r46]
            android.support.constraint.solver.widgets.ResolutionAnchor r6 = r6.getResolutionNode()
            android.support.constraint.solver.widgets.ResolutionAnchor r7 = r10.resolvedTarget
            r6.resolve(r7, r3)
            android.support.constraint.solver.widgets.ConstraintAnchor[] r6 = r11.mListAnchors
            int r7 = r46 + 1
            r6 = r6[r7]
            android.support.constraint.solver.widgets.ResolutionAnchor r6 = r6.getResolutionNode()
            android.support.constraint.solver.widgets.ResolutionAnchor r7 = r10.resolvedTarget
            float r9 = r3 + r2
            r6.resolve(r7, r9)
            android.support.constraint.solver.widgets.ConstraintAnchor[] r6 = r11.mListAnchors
            r6 = r6[r46]
            android.support.constraint.solver.widgets.ResolutionAnchor r6 = r6.getResolutionNode()
            r6.addResolvedValue(r13)
            android.support.constraint.solver.widgets.ConstraintAnchor[] r6 = r11.mListAnchors
            int r7 = r46 + 1
            r6 = r6[r7]
            android.support.constraint.solver.widgets.ResolutionAnchor r6 = r6.getResolutionNode()
            r6.addResolvedValue(r13)
            float r3 = r3 + r2
            android.support.constraint.solver.widgets.ConstraintAnchor[] r6 = r11.mListAnchors
            int r7 = r46 + 1
            r6 = r6[r7]
            int r6 = r6.getMargin()
            float r6 = (float) r6
            float r23 = r3 + r6
        L_0x037f:
            r11 = r17
            r3 = r37
            r2 = r38
            r7 = r39
            goto L_0x02ef
        L_0x0389:
            r38 = r2
            r39 = r7
            r41 = r0
            r9 = r3
            r40 = r34
            goto L_0x04a8
        L_0x0394:
            r38 = r2
            r37 = r3
            r39 = r7
            if (r8 != 0) goto L_0x03a7
            if (r22 == 0) goto L_0x039f
            goto L_0x03a7
        L_0x039f:
            r41 = r0
            r40 = r34
            r9 = r37
            goto L_0x04a8
        L_0x03a7:
            if (r8 == 0) goto L_0x03ac
            float r23 = r23 - r0
            goto L_0x03b0
        L_0x03ac:
            if (r22 == 0) goto L_0x03b0
            float r23 = r23 - r0
        L_0x03b0:
            r2 = r37
            int r9 = r34 + 1
            float r3 = (float) r9
            float r3 = r23 / r3
            if (r22 == 0) goto L_0x03c9
            r6 = r34
            r7 = 1
            if (r6 <= r7) goto L_0x03c4
            int r9 = r6 + -1
            float r7 = (float) r9
            float r3 = r23 / r7
            goto L_0x03cb
        L_0x03c4:
            r7 = 1073741824(0x40000000, float:2.0)
            float r3 = r23 / r7
            goto L_0x03cb
        L_0x03c9:
            r6 = r34
        L_0x03cb:
            r7 = r36
            r9 = r37
            int r11 = r9.getVisibility()
            r14 = 8
            if (r11 == r14) goto L_0x03d8
            float r7 = r7 + r3
        L_0x03d8:
            if (r22 == 0) goto L_0x03e8
            r11 = 1
            if (r6 <= r11) goto L_0x03e8
            android.support.constraint.solver.widgets.ConstraintAnchor[] r11 = r5.mListAnchors
            r11 = r11[r46]
            int r11 = r11.getMargin()
            float r11 = (float) r11
            float r7 = r36 + r11
        L_0x03e8:
            if (r8 == 0) goto L_0x03f6
            if (r5 == 0) goto L_0x03f6
            android.support.constraint.solver.widgets.ConstraintAnchor[] r11 = r5.mListAnchors
            r11 = r11[r46]
            int r11 = r11.getMargin()
            float r11 = (float) r11
            float r7 = r7 + r11
        L_0x03f6:
            r11 = r2
            r23 = r7
        L_0x03f9:
            if (r11 == 0) goto L_0x04a4
            android.support.constraint.solver.Metrics r2 = android.support.constraint.solver.LinearSystem.sMetrics
            if (r2 == 0) goto L_0x041a
            android.support.constraint.solver.Metrics r2 = android.support.constraint.solver.LinearSystem.sMetrics
            r40 = r6
            long r6 = r2.nonresolvedWidgets
            long r6 = r6 - r27
            r2.nonresolvedWidgets = r6
            android.support.constraint.solver.Metrics r2 = android.support.constraint.solver.LinearSystem.sMetrics
            long r6 = r2.resolvedWidgets
            long r6 = r6 + r27
            r2.resolvedWidgets = r6
            android.support.constraint.solver.Metrics r2 = android.support.constraint.solver.LinearSystem.sMetrics
            long r6 = r2.chainConnectionResolved
            long r6 = r6 + r27
            r2.chainConnectionResolved = r6
            goto L_0x041c
        L_0x041a:
            r40 = r6
        L_0x041c:
            android.support.constraint.solver.widgets.ConstraintWidget[] r2 = r11.mNextChainWidget
            r2 = r2[r1]
            if (r2 != 0) goto L_0x042a
            if (r11 != r4) goto L_0x0425
            goto L_0x042a
        L_0x0425:
            r41 = r0
        L_0x0427:
            r1 = 8
            goto L_0x0499
        L_0x042a:
            r6 = 0
            if (r1 != 0) goto L_0x0433
            int r7 = r11.getWidth()
            float r6 = (float) r7
            goto L_0x0438
        L_0x0433:
            int r7 = r11.getHeight()
            float r6 = (float) r7
        L_0x0438:
            if (r11 == r5) goto L_0x0445
            android.support.constraint.solver.widgets.ConstraintAnchor[] r7 = r11.mListAnchors
            r7 = r7[r46]
            int r7 = r7.getMargin()
            float r7 = (float) r7
            float r23 = r23 + r7
        L_0x0445:
            r7 = r23
            android.support.constraint.solver.widgets.ConstraintAnchor[] r14 = r11.mListAnchors
            r14 = r14[r46]
            android.support.constraint.solver.widgets.ResolutionAnchor r14 = r14.getResolutionNode()
            r41 = r0
            android.support.constraint.solver.widgets.ResolutionAnchor r0 = r10.resolvedTarget
            r14.resolve(r0, r7)
            android.support.constraint.solver.widgets.ConstraintAnchor[] r0 = r11.mListAnchors
            int r14 = r46 + 1
            r0 = r0[r14]
            android.support.constraint.solver.widgets.ResolutionAnchor r0 = r0.getResolutionNode()
            android.support.constraint.solver.widgets.ResolutionAnchor r14 = r10.resolvedTarget
            float r1 = r7 + r6
            r0.resolve(r14, r1)
            android.support.constraint.solver.widgets.ConstraintAnchor[] r0 = r11.mListAnchors
            r0 = r0[r46]
            android.support.constraint.solver.widgets.ResolutionAnchor r0 = r0.getResolutionNode()
            r0.addResolvedValue(r13)
            android.support.constraint.solver.widgets.ConstraintAnchor[] r0 = r11.mListAnchors
            int r1 = r46 + 1
            r0 = r0[r1]
            android.support.constraint.solver.widgets.ResolutionAnchor r0 = r0.getResolutionNode()
            r0.addResolvedValue(r13)
            android.support.constraint.solver.widgets.ConstraintAnchor[] r0 = r11.mListAnchors
            int r1 = r46 + 1
            r0 = r0[r1]
            int r0 = r0.getMargin()
            float r0 = (float) r0
            float r0 = r0 + r6
            float r23 = r7 + r0
            if (r2 == 0) goto L_0x0427
            int r0 = r2.getVisibility()
            r1 = 8
            if (r0 == r1) goto L_0x0499
            float r23 = r23 + r3
        L_0x0499:
            r11 = r2
            r17 = r2
            r6 = r40
            r0 = r41
            r1 = r45
            goto L_0x03f9
        L_0x04a4:
            r41 = r0
            r40 = r6
        L_0x04a8:
            r0 = 1
            return r0
        L_0x04aa:
            r30 = r2
            r32 = r6
            r39 = r7
            r33 = r8
            r40 = r9
            r35 = r13
            r13 = r44
            r9 = r3
        L_0x04b9:
            return r16
        L_0x04ba:
            r30 = r2
            r32 = r6
            r39 = r7
            r33 = r8
            r40 = r9
            r35 = r13
            r13 = r0
            r9 = r3
        L_0x04c8:
            return r16
        */
        throw new UnsupportedOperationException("Method not decompiled: android.support.constraint.solver.widgets.Optimizer.applyChainOptimized(android.support.constraint.solver.widgets.ConstraintWidgetContainer, android.support.constraint.solver.LinearSystem, int, int, android.support.constraint.solver.widgets.ChainHead):boolean");
    }

    static void setOptimizedWidget(ConstraintWidget widget, int orientation, int resolvedOffset) {
        int startOffset = orientation * 2;
        int endOffset = startOffset + 1;
        widget.mListAnchors[startOffset].getResolutionNode().resolvedTarget = widget.getParent().mLeft.getResolutionNode();
        widget.mListAnchors[startOffset].getResolutionNode().resolvedOffset = (float) resolvedOffset;
        widget.mListAnchors[startOffset].getResolutionNode().state = 1;
        widget.mListAnchors[endOffset].getResolutionNode().resolvedTarget = widget.mListAnchors[startOffset].getResolutionNode();
        widget.mListAnchors[endOffset].getResolutionNode().resolvedOffset = (float) widget.getLength(orientation);
        widget.mListAnchors[endOffset].getResolutionNode().state = 1;
    }
}
