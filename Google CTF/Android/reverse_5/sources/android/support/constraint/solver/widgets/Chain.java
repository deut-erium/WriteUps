package android.support.constraint.solver.widgets;

import android.support.constraint.solver.LinearSystem;

class Chain {
    private static final boolean DEBUG = false;

    Chain() {
    }

    static void applyChainConstraints(ConstraintWidgetContainer constraintWidgetContainer, LinearSystem system, int orientation) {
        ChainHead[] chainsArray;
        int chainsSize;
        int offset;
        if (orientation == 0) {
            offset = 0;
            chainsSize = constraintWidgetContainer.mHorizontalChainsSize;
            chainsArray = constraintWidgetContainer.mHorizontalChainsArray;
        } else {
            offset = 2;
            chainsSize = constraintWidgetContainer.mVerticalChainsSize;
            chainsArray = constraintWidgetContainer.mVerticalChainsArray;
        }
        for (int i = 0; i < chainsSize; i++) {
            ChainHead first = chainsArray[i];
            first.define();
            if (!constraintWidgetContainer.optimizeFor(4)) {
                applyChainConstraints(constraintWidgetContainer, system, orientation, offset, first);
            } else if (!Optimizer.applyChainOptimized(constraintWidgetContainer, system, orientation, offset, first)) {
                applyChainConstraints(constraintWidgetContainer, system, orientation, offset, first);
            }
        }
    }

    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r14v0, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r3v5, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r3v8, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r3v9, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r3v10, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r60v0, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r14v1, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r60v1, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r14v2, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r60v2, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r14v3, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r60v3, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r60v4, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r60v5, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r60v6, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r60v7, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r1v31, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r1v34, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r1v53, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r14v5, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r14v7, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r7v8, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r34v0, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r34v1, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r34v2, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r34v3, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r0v6, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r0v7, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r0v8, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r0v9, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r0v10, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r3v90, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r2v73, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r3v99, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r3v100, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r2v75, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r2v76, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r2v77, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX DEBUG: Multi-variable search result rejected for TypeSearchVarInfo{r3v105, resolved type: android.support.constraint.solver.widgets.ConstraintWidget} */
    /* JADX WARNING: Multi-variable type inference failed */
    /* JADX WARNING: Removed duplicated region for block: B:284:0x061c A[ADDED_TO_REGION] */
    /* JADX WARNING: Removed duplicated region for block: B:287:0x0625  */
    /* JADX WARNING: Removed duplicated region for block: B:313:0x06a5  */
    /* Code decompiled incorrectly, please refer to instructions dump. */
    static void applyChainConstraints(android.support.constraint.solver.widgets.ConstraintWidgetContainer r62, android.support.constraint.solver.LinearSystem r63, int r64, int r65, android.support.constraint.solver.widgets.ChainHead r66) {
        /*
            r0 = r62
            r10 = r63
            r12 = r66
            android.support.constraint.solver.widgets.ConstraintWidget r13 = r12.mFirst
            android.support.constraint.solver.widgets.ConstraintWidget r14 = r12.mLast
            android.support.constraint.solver.widgets.ConstraintWidget r9 = r12.mFirstVisibleWidget
            android.support.constraint.solver.widgets.ConstraintWidget r8 = r12.mLastVisibleWidget
            android.support.constraint.solver.widgets.ConstraintWidget r7 = r12.mHead
            r1 = r13
            r2 = 0
            r3 = 0
            float r4 = r12.mTotalWeight
            android.support.constraint.solver.widgets.ConstraintWidget r6 = r12.mFirstMatchConstraintWidget
            android.support.constraint.solver.widgets.ConstraintWidget r5 = r12.mLastMatchConstraintWidget
            r15 = r1
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r1 = r0.mListDimensionBehaviors
            r1 = r1[r64]
            r16 = r2
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r2 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.WRAP_CONTENT
            r17 = r3
            if (r1 != r2) goto L_0x0028
            r1 = 1
            goto L_0x0029
        L_0x0028:
            r1 = 0
        L_0x0029:
            r19 = r1
            r1 = 0
            r2 = 0
            r20 = 0
            if (r64 != 0) goto L_0x0054
            int r3 = r7.mHorizontalChainStyle
            if (r3 != 0) goto L_0x0037
            r3 = 1
            goto L_0x0038
        L_0x0037:
            r3 = 0
        L_0x0038:
            r1 = r3
            int r3 = r7.mHorizontalChainStyle
            r23 = r1
            r1 = 1
            if (r3 != r1) goto L_0x0042
            r1 = 1
            goto L_0x0043
        L_0x0042:
            r1 = 0
        L_0x0043:
            int r2 = r7.mHorizontalChainStyle
            r3 = 2
            if (r2 != r3) goto L_0x004a
            r2 = 1
            goto L_0x004b
        L_0x004a:
            r2 = 0
        L_0x004b:
            r3 = r15
            r20 = r16
            r24 = r23
        L_0x0050:
            r16 = r1
            r15 = r2
            goto L_0x0072
        L_0x0054:
            int r3 = r7.mVerticalChainStyle
            if (r3 != 0) goto L_0x005a
            r3 = 1
            goto L_0x005b
        L_0x005a:
            r3 = 0
        L_0x005b:
            r1 = r3
            int r3 = r7.mVerticalChainStyle
            r24 = r1
            r1 = 1
            if (r3 != r1) goto L_0x0065
            r1 = 1
            goto L_0x0066
        L_0x0065:
            r1 = 0
        L_0x0066:
            int r2 = r7.mVerticalChainStyle
            r3 = 2
            if (r2 != r3) goto L_0x006d
            r2 = 1
            goto L_0x006e
        L_0x006d:
            r2 = 0
        L_0x006e:
            r3 = r15
            r20 = r16
            goto L_0x0050
        L_0x0072:
            r25 = r5
            if (r17 != 0) goto L_0x0154
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r3.mListAnchors
            r2 = r2[r65]
            r22 = 4
            if (r19 != 0) goto L_0x0080
            if (r15 == 0) goto L_0x0082
        L_0x0080:
            r22 = 1
        L_0x0082:
            int r23 = r2.getMargin()
            android.support.constraint.solver.widgets.ConstraintAnchor r1 = r2.mTarget
            if (r1 == 0) goto L_0x0094
            if (r3 == r13) goto L_0x0094
            android.support.constraint.solver.widgets.ConstraintAnchor r1 = r2.mTarget
            int r1 = r1.getMargin()
            int r23 = r23 + r1
        L_0x0094:
            r1 = r23
            if (r15 == 0) goto L_0x009f
            if (r3 == r13) goto L_0x009f
            if (r3 == r9) goto L_0x009f
            r22 = 6
            goto L_0x00a5
        L_0x009f:
            if (r24 == 0) goto L_0x00a5
            if (r19 == 0) goto L_0x00a5
            r22 = 4
        L_0x00a5:
            r28 = r22
            android.support.constraint.solver.widgets.ConstraintAnchor r5 = r2.mTarget
            if (r5 == 0) goto L_0x00d6
            if (r3 != r9) goto L_0x00bc
            android.support.constraint.solver.SolverVariable r5 = r2.mSolverVariable
            r30 = r4
            android.support.constraint.solver.widgets.ConstraintAnchor r4 = r2.mTarget
            android.support.constraint.solver.SolverVariable r4 = r4.mSolverVariable
            r31 = r6
            r6 = 5
            r10.addGreaterThan(r5, r4, r1, r6)
            goto L_0x00ca
        L_0x00bc:
            r30 = r4
            r31 = r6
            android.support.constraint.solver.SolverVariable r4 = r2.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor r5 = r2.mTarget
            android.support.constraint.solver.SolverVariable r5 = r5.mSolverVariable
            r6 = 6
            r10.addGreaterThan(r4, r5, r1, r6)
        L_0x00ca:
            android.support.constraint.solver.SolverVariable r4 = r2.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor r5 = r2.mTarget
            android.support.constraint.solver.SolverVariable r5 = r5.mSolverVariable
            r6 = r28
            r10.addEquality(r4, r5, r1, r6)
            goto L_0x00dc
        L_0x00d6:
            r30 = r4
            r31 = r6
            r6 = r28
        L_0x00dc:
            if (r19 == 0) goto L_0x011c
            int r4 = r3.getVisibility()
            r5 = 8
            if (r4 == r5) goto L_0x0106
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour[] r4 = r3.mListDimensionBehaviors
            r4 = r4[r64]
            android.support.constraint.solver.widgets.ConstraintWidget$DimensionBehaviour r5 = android.support.constraint.solver.widgets.ConstraintWidget.DimensionBehaviour.MATCH_CONSTRAINT
            if (r4 != r5) goto L_0x0106
            android.support.constraint.solver.widgets.ConstraintAnchor[] r4 = r3.mListAnchors
            int r5 = r65 + 1
            r4 = r4[r5]
            android.support.constraint.solver.SolverVariable r4 = r4.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor[] r5 = r3.mListAnchors
            r5 = r5[r65]
            android.support.constraint.solver.SolverVariable r5 = r5.mSolverVariable
            r32 = r1
            r33 = r2
            r1 = 0
            r2 = 5
            r10.addGreaterThan(r4, r5, r1, r2)
            goto L_0x010b
        L_0x0106:
            r32 = r1
            r33 = r2
            r1 = 0
        L_0x010b:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r3.mListAnchors
            r2 = r2[r65]
            android.support.constraint.solver.SolverVariable r2 = r2.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor[] r4 = r0.mListAnchors
            r4 = r4[r65]
            android.support.constraint.solver.SolverVariable r4 = r4.mSolverVariable
            r5 = 6
            r10.addGreaterThan(r2, r4, r1, r5)
            goto L_0x0120
        L_0x011c:
            r32 = r1
            r33 = r2
        L_0x0120:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r3.mListAnchors
            int r2 = r65 + 1
            r1 = r1[r2]
            android.support.constraint.solver.widgets.ConstraintAnchor r1 = r1.mTarget
            if (r1 == 0) goto L_0x0140
            android.support.constraint.solver.widgets.ConstraintWidget r2 = r1.mOwner
            android.support.constraint.solver.widgets.ConstraintAnchor[] r4 = r2.mListAnchors
            r4 = r4[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor r4 = r4.mTarget
            if (r4 == 0) goto L_0x013e
            android.support.constraint.solver.widgets.ConstraintAnchor[] r4 = r2.mListAnchors
            r4 = r4[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor r4 = r4.mTarget
            android.support.constraint.solver.widgets.ConstraintWidget r4 = r4.mOwner
            if (r4 == r3) goto L_0x0141
        L_0x013e:
            r2 = 0
            goto L_0x0141
        L_0x0140:
            r2 = 0
        L_0x0141:
            r20 = r2
            if (r20 == 0) goto L_0x0149
            r2 = r20
            r3 = r2
            goto L_0x014c
        L_0x0149:
            r1 = 1
            r17 = r1
        L_0x014c:
            r5 = r25
            r4 = r30
            r6 = r31
            goto L_0x0072
        L_0x0154:
            r30 = r4
            r31 = r6
            if (r8 == 0) goto L_0x0180
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r14.mListAnchors
            int r2 = r65 + 1
            r1 = r1[r2]
            android.support.constraint.solver.widgets.ConstraintAnchor r1 = r1.mTarget
            if (r1 == 0) goto L_0x0180
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r8.mListAnchors
            int r2 = r65 + 1
            r1 = r1[r2]
            android.support.constraint.solver.SolverVariable r2 = r1.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor[] r4 = r14.mListAnchors
            int r5 = r65 + 1
            r4 = r4[r5]
            android.support.constraint.solver.widgets.ConstraintAnchor r4 = r4.mTarget
            android.support.constraint.solver.SolverVariable r4 = r4.mSolverVariable
            int r5 = r1.getMargin()
            int r5 = -r5
            r6 = 5
            r10.addLowerThan(r2, r4, r5, r6)
            goto L_0x0181
        L_0x0180:
            r6 = 5
        L_0x0181:
            if (r19 == 0) goto L_0x01a1
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r0.mListAnchors
            int r2 = r65 + 1
            r1 = r1[r2]
            android.support.constraint.solver.SolverVariable r1 = r1.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r14.mListAnchors
            int r4 = r65 + 1
            r2 = r2[r4]
            android.support.constraint.solver.SolverVariable r2 = r2.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor[] r4 = r14.mListAnchors
            int r5 = r65 + 1
            r4 = r4[r5]
            int r4 = r4.getMargin()
            r5 = 6
            r10.addGreaterThan(r1, r2, r4, r5)
        L_0x01a1:
            java.util.ArrayList<android.support.constraint.solver.widgets.ConstraintWidget> r5 = r12.mWeightedMatchConstraintsWidgets
            if (r5 == 0) goto L_0x0272
            int r1 = r5.size()
            r2 = 1
            if (r1 <= r2) goto L_0x0272
            r4 = 0
            r21 = 0
            boolean r2 = r12.mHasUndefinedWeights
            if (r2 == 0) goto L_0x01bc
            boolean r2 = r12.mHasComplexMatchWeights
            if (r2 != 0) goto L_0x01bc
            int r2 = r12.mWidgetsMatchCount
            float r2 = (float) r2
            r30 = r2
        L_0x01bc:
            r2 = 0
        L_0x01bd:
            if (r2 >= r1) goto L_0x0272
            java.lang.Object r22 = r5.get(r2)
            r6 = r22
            android.support.constraint.solver.widgets.ConstraintWidget r6 = (android.support.constraint.solver.widgets.ConstraintWidget) r6
            float[] r0 = r6.mWeight
            r0 = r0[r64]
            r22 = 0
            int r23 = (r0 > r22 ? 1 : (r0 == r22 ? 0 : -1))
            if (r23 >= 0) goto L_0x0200
            r43 = r0
            boolean r0 = r12.mHasComplexMatchWeights
            if (r0 == 0) goto L_0x01f5
            android.support.constraint.solver.widgets.ConstraintAnchor[] r0 = r6.mListAnchors
            int r22 = r65 + 1
            r0 = r0[r22]
            android.support.constraint.solver.SolverVariable r0 = r0.mSolverVariable
            r44 = r1
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r6.mListAnchors
            r1 = r1[r65]
            android.support.constraint.solver.SolverVariable r1 = r1.mSolverVariable
            r45 = r3
            r3 = 4
            r46 = r5
            r5 = 0
            r10.addEquality(r0, r1, r5, r3)
            r3 = 0
            r5 = 6
            goto L_0x0265
        L_0x01f5:
            r44 = r1
            r45 = r3
            r46 = r5
            r0 = 1065353216(0x3f800000, float:1.0)
            r43 = r0
            goto L_0x0208
        L_0x0200:
            r43 = r0
            r44 = r1
            r45 = r3
            r46 = r5
        L_0x0208:
            int r0 = (r43 > r22 ? 1 : (r43 == r22 ? 0 : -1))
            if (r0 != 0) goto L_0x0220
            android.support.constraint.solver.widgets.ConstraintAnchor[] r0 = r6.mListAnchors
            int r1 = r65 + 1
            r0 = r0[r1]
            android.support.constraint.solver.SolverVariable r0 = r0.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r6.mListAnchors
            r1 = r1[r65]
            android.support.constraint.solver.SolverVariable r1 = r1.mSolverVariable
            r3 = 0
            r5 = 6
            r10.addEquality(r0, r1, r3, r5)
            goto L_0x0265
        L_0x0220:
            r3 = 0
            r5 = 6
            if (r4 == 0) goto L_0x025d
            android.support.constraint.solver.widgets.ConstraintAnchor[] r0 = r4.mListAnchors
            r0 = r0[r65]
            android.support.constraint.solver.SolverVariable r0 = r0.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r4.mListAnchors
            int r18 = r65 + 1
            r1 = r1[r18]
            android.support.constraint.solver.SolverVariable r1 = r1.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r6.mListAnchors
            r3 = r3[r65]
            android.support.constraint.solver.SolverVariable r3 = r3.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor[] r5 = r6.mListAnchors
            int r18 = r65 + 1
            r5 = r5[r18]
            android.support.constraint.solver.SolverVariable r5 = r5.mSolverVariable
            r48 = r4
            android.support.constraint.solver.ArrayRow r4 = r63.createRow()
            r35 = r4
            r36 = r21
            r37 = r30
            r38 = r43
            r39 = r0
            r40 = r1
            r41 = r3
            r42 = r5
            r35.createRowEqualMatchDimensions(r36, r37, r38, r39, r40, r41, r42)
            r10.addConstraint(r4)
            goto L_0x025f
        L_0x025d:
            r48 = r4
        L_0x025f:
            r0 = r6
            r1 = r43
            r4 = r0
            r21 = r1
        L_0x0265:
            int r2 = r2 + 1
            r1 = r44
            r3 = r45
            r5 = r46
            r0 = r62
            r6 = 5
            goto L_0x01bd
        L_0x0272:
            r45 = r3
            r46 = r5
            if (r9 == 0) goto L_0x0319
            if (r9 == r8) goto L_0x0287
            if (r15 == 0) goto L_0x027d
            goto L_0x0287
        L_0x027d:
            r35 = r7
            r0 = r8
            r10 = r9
            r28 = r45
            r32 = r46
            goto L_0x0321
        L_0x0287:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r13.mListAnchors
            r1 = r1[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r14.mListAnchors
            int r3 = r65 + 1
            r2 = r2[r3]
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r13.mListAnchors
            r3 = r3[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r3.mTarget
            if (r3 == 0) goto L_0x02a2
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r13.mListAnchors
            r3 = r3[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r3.mTarget
            android.support.constraint.solver.SolverVariable r3 = r3.mSolverVariable
            goto L_0x02a3
        L_0x02a2:
            r3 = 0
        L_0x02a3:
            r18 = r3
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r14.mListAnchors
            int r4 = r65 + 1
            r3 = r3[r4]
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r3.mTarget
            if (r3 == 0) goto L_0x02ba
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r14.mListAnchors
            int r4 = r65 + 1
            r3 = r3[r4]
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r3.mTarget
            android.support.constraint.solver.SolverVariable r3 = r3.mSolverVariable
            goto L_0x02bb
        L_0x02ba:
            r3 = 0
        L_0x02bb:
            r21 = r3
            if (r9 != r8) goto L_0x02c9
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r9.mListAnchors
            r1 = r3[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r9.mListAnchors
            int r4 = r65 + 1
            r2 = r3[r4]
        L_0x02c9:
            r6 = r1
            r5 = r2
            if (r18 == 0) goto L_0x030a
            if (r21 == 0) goto L_0x030a
            r1 = 1056964608(0x3f000000, float:0.5)
            if (r64 != 0) goto L_0x02d8
            float r1 = r7.mHorizontalBiasPercent
        L_0x02d5:
            r22 = r1
            goto L_0x02db
        L_0x02d8:
            float r1 = r7.mVerticalBiasPercent
            goto L_0x02d5
        L_0x02db:
            int r23 = r6.getMargin()
            int r26 = r5.getMargin()
            android.support.constraint.solver.SolverVariable r2 = r6.mSolverVariable
            android.support.constraint.solver.SolverVariable r4 = r5.mSolverVariable
            r27 = 5
            r1 = r10
            r28 = r45
            r3 = r18
            r29 = r4
            r4 = r23
            r33 = r5
            r32 = r46
            r5 = r22
            r34 = r6
            r6 = r21
            r35 = r7
            r7 = r29
            r0 = r8
            r8 = r26
            r10 = r9
            r9 = r27
            r1.addCentering(r2, r3, r4, r5, r6, r7, r8, r9)
            goto L_0x0312
        L_0x030a:
            r35 = r7
            r0 = r8
            r10 = r9
            r28 = r45
            r32 = r46
        L_0x0312:
            r60 = r14
            r14 = r10
            r10 = r63
            goto L_0x0618
        L_0x0319:
            r35 = r7
            r0 = r8
            r10 = r9
            r28 = r45
            r32 = r46
        L_0x0321:
            if (r24 == 0) goto L_0x047e
            if (r10 == 0) goto L_0x047e
            r1 = r10
            r2 = r10
            int r3 = r12.mWidgetsMatchCount
            if (r3 <= 0) goto L_0x0334
            int r3 = r12.mWidgetsCount
            int r4 = r12.mWidgetsMatchCount
            if (r3 != r4) goto L_0x0334
            r47 = 1
            goto L_0x0336
        L_0x0334:
            r47 = 0
        L_0x0336:
            r9 = r1
            r8 = r2
        L_0x0338:
            if (r9 == 0) goto L_0x0470
            android.support.constraint.solver.widgets.ConstraintWidget[] r1 = r9.mNextChainWidget
            r1 = r1[r64]
            r7 = r1
        L_0x033f:
            if (r7 == 0) goto L_0x034e
            int r1 = r7.getVisibility()
            r2 = 8
            if (r1 != r2) goto L_0x0350
            android.support.constraint.solver.widgets.ConstraintWidget[] r1 = r7.mNextChainWidget
            r7 = r1[r64]
            goto L_0x033f
        L_0x034e:
            r2 = 8
        L_0x0350:
            if (r7 != 0) goto L_0x0362
            if (r9 != r0) goto L_0x0355
            goto L_0x0362
        L_0x0355:
            r34 = r7
            r36 = r8
            r53 = r10
            r52 = r14
            r10 = r63
            r14 = r9
            goto L_0x0459
        L_0x0362:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r9.mListAnchors
            r6 = r1[r65]
            android.support.constraint.solver.SolverVariable r5 = r6.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor r1 = r6.mTarget
            if (r1 == 0) goto L_0x0371
            android.support.constraint.solver.widgets.ConstraintAnchor r1 = r6.mTarget
            android.support.constraint.solver.SolverVariable r1 = r1.mSolverVariable
            goto L_0x0372
        L_0x0371:
            r1 = 0
        L_0x0372:
            if (r8 == r9) goto L_0x037f
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r8.mListAnchors
            int r4 = r65 + 1
            r3 = r3[r4]
            android.support.constraint.solver.SolverVariable r1 = r3.mSolverVariable
        L_0x037c:
            r18 = r1
            goto L_0x0397
        L_0x037f:
            if (r9 != r10) goto L_0x037c
            if (r8 != r9) goto L_0x037c
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r13.mListAnchors
            r3 = r3[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r3.mTarget
            if (r3 == 0) goto L_0x0394
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r13.mListAnchors
            r3 = r3[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r3.mTarget
            android.support.constraint.solver.SolverVariable r3 = r3.mSolverVariable
            goto L_0x0395
        L_0x0394:
            r3 = 0
        L_0x0395:
            r1 = r3
            goto L_0x037c
        L_0x0397:
            r1 = 0
            r3 = 0
            r4 = 0
            int r20 = r6.getMargin()
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r9.mListAnchors
            int r21 = r65 + 1
            r2 = r2[r21]
            int r2 = r2.getMargin()
            if (r7 == 0) goto L_0x03c3
            r49 = r1
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r7.mListAnchors
            r1 = r1[r65]
            android.support.constraint.solver.SolverVariable r3 = r1.mSolverVariable
            r50 = r1
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r9.mListAnchors
            int r21 = r65 + 1
            r1 = r1[r21]
            android.support.constraint.solver.SolverVariable r1 = r1.mSolverVariable
            r22 = r1
            r21 = r3
            r4 = r50
            goto L_0x03e1
        L_0x03c3:
            r49 = r1
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r14.mListAnchors
            int r21 = r65 + 1
            r1 = r1[r21]
            android.support.constraint.solver.widgets.ConstraintAnchor r1 = r1.mTarget
            if (r1 == 0) goto L_0x03d1
            android.support.constraint.solver.SolverVariable r3 = r1.mSolverVariable
        L_0x03d1:
            r51 = r1
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r9.mListAnchors
            int r21 = r65 + 1
            r1 = r1[r21]
            android.support.constraint.solver.SolverVariable r1 = r1.mSolverVariable
            r22 = r1
            r21 = r3
            r4 = r51
        L_0x03e1:
            if (r4 == 0) goto L_0x03e8
            int r1 = r4.getMargin()
            int r2 = r2 + r1
        L_0x03e8:
            r23 = r2
            if (r8 == 0) goto L_0x03f8
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r8.mListAnchors
            int r2 = r65 + 1
            r1 = r1[r2]
            int r1 = r1.getMargin()
            int r20 = r20 + r1
        L_0x03f8:
            if (r5 == 0) goto L_0x044e
            if (r18 == 0) goto L_0x044e
            if (r21 == 0) goto L_0x044e
            if (r22 == 0) goto L_0x044e
            r1 = r20
            if (r9 != r10) goto L_0x040c
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r10.mListAnchors
            r2 = r2[r65]
            int r1 = r2.getMargin()
        L_0x040c:
            r26 = r1
            r1 = r23
            if (r9 != r0) goto L_0x041c
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r0.mListAnchors
            int r3 = r65 + 1
            r2 = r2[r3]
            int r1 = r2.getMargin()
        L_0x041c:
            r27 = r1
            r1 = 4
            if (r47 == 0) goto L_0x0422
            r1 = 6
        L_0x0422:
            r28 = r1
            r29 = 1056964608(0x3f000000, float:0.5)
            r3 = r10
            r10 = r63
            r1 = r10
            r52 = r14
            r14 = 8
            r2 = r5
            r53 = r3
            r3 = r18
            r50 = r4
            r4 = r26
            r33 = r5
            r5 = r29
            r29 = r6
            r6 = r21
            r34 = r7
            r7 = r22
            r36 = r8
            r8 = r27
            r14 = r9
            r9 = r28
            r1.addCentering(r2, r3, r4, r5, r6, r7, r8, r9)
            goto L_0x0459
        L_0x044e:
            r34 = r7
            r36 = r8
            r53 = r10
            r52 = r14
            r10 = r63
            r14 = r9
        L_0x0459:
            int r1 = r14.getVisibility()
            r2 = 8
            if (r1 == r2) goto L_0x0464
            r1 = r14
            r8 = r1
            goto L_0x0466
        L_0x0464:
            r8 = r36
        L_0x0466:
            r9 = r34
            r20 = r34
            r14 = r52
            r10 = r53
            goto L_0x0338
        L_0x0470:
            r53 = r10
            r52 = r14
            r10 = r63
            r14 = r9
            r11 = r14
            r60 = r52
            r14 = r53
            goto L_0x061a
        L_0x047e:
            r53 = r10
            r52 = r14
            r10 = r63
            if (r16 == 0) goto L_0x0614
            r14 = r53
            if (r14 == 0) goto L_0x0611
            r1 = r14
            r2 = r14
            int r3 = r12.mWidgetsMatchCount
            if (r3 <= 0) goto L_0x0499
            int r3 = r12.mWidgetsCount
            int r4 = r12.mWidgetsMatchCount
            if (r3 != r4) goto L_0x0499
            r47 = 1
            goto L_0x049b
        L_0x0499:
            r47 = 0
        L_0x049b:
            r9 = r1
            r8 = r2
        L_0x049d:
            if (r9 == 0) goto L_0x0587
            android.support.constraint.solver.widgets.ConstraintWidget[] r1 = r9.mNextChainWidget
            r1 = r1[r64]
        L_0x04a3:
            if (r1 == 0) goto L_0x04b2
            int r2 = r1.getVisibility()
            r3 = 8
            if (r2 != r3) goto L_0x04b2
            android.support.constraint.solver.widgets.ConstraintWidget[] r2 = r1.mNextChainWidget
            r1 = r2[r64]
            goto L_0x04a3
        L_0x04b2:
            if (r9 == r14) goto L_0x0571
            if (r9 == r0) goto L_0x0571
            if (r1 == 0) goto L_0x0571
            if (r1 != r0) goto L_0x04bb
            r1 = 0
        L_0x04bb:
            r7 = r1
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r9.mListAnchors
            r6 = r1[r65]
            android.support.constraint.solver.SolverVariable r5 = r6.mSolverVariable
            android.support.constraint.solver.widgets.ConstraintAnchor r1 = r6.mTarget
            if (r1 == 0) goto L_0x04cb
            android.support.constraint.solver.widgets.ConstraintAnchor r1 = r6.mTarget
            android.support.constraint.solver.SolverVariable r1 = r1.mSolverVariable
            goto L_0x04cc
        L_0x04cb:
            r1 = 0
        L_0x04cc:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r8.mListAnchors
            int r3 = r65 + 1
            r2 = r2[r3]
            android.support.constraint.solver.SolverVariable r4 = r2.mSolverVariable
            r1 = 0
            r2 = 0
            r3 = 0
            int r18 = r6.getMargin()
            r54 = r1
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r9.mListAnchors
            int r20 = r65 + 1
            r1 = r1[r20]
            int r1 = r1.getMargin()
            if (r7 == 0) goto L_0x0504
            r55 = r2
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r7.mListAnchors
            r2 = r2[r65]
            r56 = r3
            android.support.constraint.solver.SolverVariable r3 = r2.mSolverVariable
            r57 = r3
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r2.mTarget
            if (r3 == 0) goto L_0x04fe
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r2.mTarget
            android.support.constraint.solver.SolverVariable r3 = r3.mSolverVariable
            goto L_0x04ff
        L_0x04fe:
            r3 = 0
        L_0x04ff:
            r20 = r3
            r55 = r57
            goto L_0x0520
        L_0x0504:
            r55 = r2
            r56 = r3
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r9.mListAnchors
            int r3 = r65 + 1
            r2 = r2[r3]
            android.support.constraint.solver.widgets.ConstraintAnchor r2 = r2.mTarget
            if (r2 == 0) goto L_0x0516
            android.support.constraint.solver.SolverVariable r3 = r2.mSolverVariable
            r55 = r3
        L_0x0516:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r9.mListAnchors
            int r20 = r65 + 1
            r3 = r3[r20]
            android.support.constraint.solver.SolverVariable r3 = r3.mSolverVariable
            r20 = r3
        L_0x0520:
            r3 = r2
            if (r3 == 0) goto L_0x0528
            int r2 = r3.getMargin()
            int r1 = r1 + r2
        L_0x0528:
            r21 = r1
            if (r8 == 0) goto L_0x0538
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r8.mListAnchors
            int r2 = r65 + 1
            r1 = r1[r2]
            int r1 = r1.getMargin()
            int r18 = r18 + r1
        L_0x0538:
            r1 = 4
            if (r47 == 0) goto L_0x053c
            r1 = 6
        L_0x053c:
            r22 = r1
            if (r5 == 0) goto L_0x0569
            if (r4 == 0) goto L_0x0569
            if (r55 == 0) goto L_0x0569
            if (r20 == 0) goto L_0x0569
            r23 = 1056964608(0x3f000000, float:0.5)
            r1 = r10
            r2 = r5
            r26 = r3
            r3 = r4
            r27 = r4
            r4 = r18
            r28 = r5
            r11 = 5
            r5 = r23
            r23 = r6
            r6 = r55
            r29 = r7
            r7 = r20
            r33 = r8
            r8 = r21
            r11 = r9
            r9 = r22
            r1.addCentering(r2, r3, r4, r5, r6, r7, r8, r9)
            goto L_0x056e
        L_0x0569:
            r29 = r7
            r33 = r8
            r11 = r9
        L_0x056e:
            r20 = r29
            goto L_0x0576
        L_0x0571:
            r33 = r8
            r11 = r9
            r20 = r1
        L_0x0576:
            int r1 = r11.getVisibility()
            r2 = 8
            if (r1 == r2) goto L_0x0581
            r1 = r11
            r8 = r1
            goto L_0x0583
        L_0x0581:
            r8 = r33
        L_0x0583:
            r9 = r20
            goto L_0x049d
        L_0x0587:
            r33 = r8
            r11 = r9
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r14.mListAnchors
            r9 = r1[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r13.mListAnchors
            r1 = r1[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor r8 = r1.mTarget
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r0.mListAnchors
            int r2 = r65 + 1
            r7 = r1[r2]
            r6 = r52
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r6.mListAnchors
            int r2 = r65 + 1
            r1 = r1[r2]
            android.support.constraint.solver.widgets.ConstraintAnchor r5 = r1.mTarget
            if (r8 == 0) goto L_0x05f1
            if (r14 == r0) goto L_0x05bf
            android.support.constraint.solver.SolverVariable r1 = r9.mSolverVariable
            android.support.constraint.solver.SolverVariable r2 = r8.mSolverVariable
            int r3 = r9.getMargin()
            r4 = 5
            r10.addEquality(r1, r2, r3, r4)
            r59 = r5
            r60 = r6
            r61 = r7
            r18 = r8
            r21 = r9
            goto L_0x05fb
        L_0x05bf:
            if (r5 == 0) goto L_0x05f1
            android.support.constraint.solver.SolverVariable r2 = r9.mSolverVariable
            android.support.constraint.solver.SolverVariable r3 = r8.mSolverVariable
            int r4 = r9.getMargin()
            r18 = 1056964608(0x3f000000, float:0.5)
            android.support.constraint.solver.SolverVariable r1 = r7.mSolverVariable
            r58 = r8
            android.support.constraint.solver.SolverVariable r8 = r5.mSolverVariable
            int r21 = r7.getMargin()
            r22 = 5
            r23 = r1
            r1 = r10
            r59 = r5
            r5 = r18
            r60 = r6
            r6 = r23
            r61 = r7
            r7 = r8
            r18 = r58
            r8 = r21
            r21 = r9
            r9 = r22
            r1.addCentering(r2, r3, r4, r5, r6, r7, r8, r9)
            goto L_0x05fb
        L_0x05f1:
            r59 = r5
            r60 = r6
            r61 = r7
            r18 = r8
            r21 = r9
        L_0x05fb:
            r1 = r59
            if (r1 == 0) goto L_0x061a
            if (r14 == r0) goto L_0x061a
            r2 = r61
            android.support.constraint.solver.SolverVariable r3 = r2.mSolverVariable
            android.support.constraint.solver.SolverVariable r4 = r1.mSolverVariable
            int r5 = r2.getMargin()
            int r5 = -r5
            r6 = 5
            r10.addEquality(r3, r4, r5, r6)
            goto L_0x061a
        L_0x0611:
            r60 = r52
            goto L_0x0618
        L_0x0614:
            r60 = r52
            r14 = r53
        L_0x0618:
            r11 = r28
        L_0x061a:
            if (r24 != 0) goto L_0x0623
            if (r16 == 0) goto L_0x061f
            goto L_0x0623
        L_0x061f:
            r33 = r60
            goto L_0x06a7
        L_0x0623:
            if (r14 == 0) goto L_0x06a5
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r14.mListAnchors
            r1 = r1[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor[] r2 = r0.mListAnchors
            int r3 = r65 + 1
            r2 = r2[r3]
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r1.mTarget
            if (r3 == 0) goto L_0x0638
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r1.mTarget
            android.support.constraint.solver.SolverVariable r3 = r3.mSolverVariable
            goto L_0x0639
        L_0x0638:
            r3 = 0
        L_0x0639:
            r18 = r3
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r2.mTarget
            if (r3 == 0) goto L_0x0644
            android.support.constraint.solver.widgets.ConstraintAnchor r3 = r2.mTarget
            android.support.constraint.solver.SolverVariable r3 = r3.mSolverVariable
            goto L_0x0645
        L_0x0644:
            r3 = 0
        L_0x0645:
            r9 = r60
            if (r9 == r0) goto L_0x065a
            android.support.constraint.solver.widgets.ConstraintAnchor[] r4 = r9.mListAnchors
            int r5 = r65 + 1
            r4 = r4[r5]
            android.support.constraint.solver.widgets.ConstraintAnchor r5 = r4.mTarget
            if (r5 == 0) goto L_0x0658
            android.support.constraint.solver.widgets.ConstraintAnchor r5 = r4.mTarget
            android.support.constraint.solver.SolverVariable r5 = r5.mSolverVariable
            goto L_0x0659
        L_0x0658:
            r5 = 0
        L_0x0659:
            r3 = r5
        L_0x065a:
            r21 = r3
            if (r14 != r0) goto L_0x0668
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r14.mListAnchors
            r1 = r3[r65]
            android.support.constraint.solver.widgets.ConstraintAnchor[] r3 = r14.mListAnchors
            int r4 = r65 + 1
            r2 = r3[r4]
        L_0x0668:
            r8 = r1
            r7 = r2
            if (r18 == 0) goto L_0x06a2
            if (r21 == 0) goto L_0x06a2
            r22 = 1056964608(0x3f000000, float:0.5)
            int r23 = r8.getMargin()
            if (r0 != 0) goto L_0x0677
            r0 = r9
        L_0x0677:
            android.support.constraint.solver.widgets.ConstraintAnchor[] r1 = r0.mListAnchors
            int r2 = r65 + 1
            r1 = r1[r2]
            int r26 = r1.getMargin()
            android.support.constraint.solver.SolverVariable r2 = r8.mSolverVariable
            android.support.constraint.solver.SolverVariable r6 = r7.mSolverVariable
            r27 = 5
            r1 = r10
            r3 = r18
            r4 = r23
            r5 = r22
            r28 = r6
            r6 = r21
            r29 = r7
            r7 = r28
            r28 = r8
            r8 = r26
            r33 = r9
            r9 = r27
            r1.addCentering(r2, r3, r4, r5, r6, r7, r8, r9)
            goto L_0x06a7
        L_0x06a2:
            r33 = r9
            goto L_0x06a7
        L_0x06a5:
            r33 = r60
        L_0x06a7:
            return
        */
        throw new UnsupportedOperationException("Method not decompiled: android.support.constraint.solver.widgets.Chain.applyChainConstraints(android.support.constraint.solver.widgets.ConstraintWidgetContainer, android.support.constraint.solver.LinearSystem, int, int, android.support.constraint.solver.widgets.ChainHead):void");
    }
}
