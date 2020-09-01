.class Lcom/google/ctf/sandbox/o$1;
.super Ljava/lang/Object;
.source "\u0151.java"

# interfaces
.implements Landroid/view/View$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/google/ctf/sandbox/o;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/google/ctf/sandbox/o;

.field final synthetic val$editText:Landroid/widget/EditText;

.field final synthetic val$textView:Landroid/widget/TextView;


# direct methods
.method constructor <init>(Lcom/google/ctf/sandbox/o;Landroid/widget/EditText;Landroid/widget/TextView;)V
    .locals 0
    .param p1, "this$0"    # Lcom/google/ctf/sandbox/o;

    .line 39
    iput-object p1, p0, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iput-object p2, p0, Lcom/google/ctf/sandbox/o$1;->val$editText:Landroid/widget/EditText;

    iput-object p3, p0, Lcom/google/ctf/sandbox/o$1;->val$textView:Landroid/widget/TextView;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/view/View;)V
    .locals 18
    .param p1, "v"    # Landroid/view/View;

    move-object/from16 v1, p0

    .line 42
    iget-object v2, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    const/4 v3, 0x0

    iput v3, v2, Lcom/google/ctf/sandbox/o;->o:I


    const/16 v2, 0x31

    const/4 v3, 0x0

    const/4 v4, 0x3

    const/4 v5, 0x2

    const/4 v6, 0x1

    const/4 v7, 0x4

    goto/16 :goto_3

    :goto_2
    goto/16 :goto_5

    .line 58
    .line 60
    .local v2, "e":Ljava/lang/Exception;
    :goto_3
    :try_start_1
    iget-object v3, v1, Lcom/google/ctf/sandbox/o$1;->val$editText:Landroid/widget/EditText;

    invoke-virtual {v3}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v3

    .line 61
    .local v3, "flagString":Ljava/lang/String;
    invoke-virtual {v3}, Ljava/lang/String;->length()I

    move-result v5

    const/16 v6, 0x30

    if-eq v5, v6, :cond_2

    .line 62
    iget-object v4, v1, Lcom/google/ctf/sandbox/o$1;->val$textView:Landroid/widget/TextView;

    const-string v5, "\u274c"

    invoke-virtual {v4, v5}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 63
    return-void

    .line 65
    :cond_2
    const/4 v5, 0x0

    .line 65
    .local v5, "i":I
    :goto_4
    invoke-virtual {v3}, Ljava/lang/String;->length()I

    move-result v6

    div-int/2addr v6, v7

    if-ge v5, v6, :cond_3

    .line 66
    iget-object v6, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget-object v6, v6, Lcom/google/ctf/sandbox/o;->o:[J

    mul-int/lit8 v8, v5, 0x4

    add-int/2addr v8, v4

    invoke-virtual {v3, v8}, Ljava/lang/String;->charAt(I)C

    move-result v8

    shl-int/lit8 v8, v8, 0x18

    int-to-long v8, v8

    aput-wide v8, v6, v5

    .line 67
    iget-object v6, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget-object v6, v6, Lcom/google/ctf/sandbox/o;->o:[J

    aget-wide v8, v6, v5

    mul-int/lit8 v10, v5, 0x4

    const/4 v11, 0x2

    add-int/2addr v10, v11

    invoke-virtual {v3, v10}, Ljava/lang/String;->charAt(I)C

    move-result v10

    shl-int/lit8 v10, v10, 0x10

    int-to-long v12, v10

    or-long/2addr v8, v12

    aput-wide v8, v6, v5

    .line 68
    iget-object v6, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget-object v6, v6, Lcom/google/ctf/sandbox/o;->o:[J

    aget-wide v8, v6, v5

    mul-int/lit8 v10, v5, 0x4

    const/4 v12, 0x1

    add-int/2addr v10, v12

    invoke-virtual {v3, v10}, Ljava/lang/String;->charAt(I)C

    move-result v10

    shl-int/lit8 v10, v10, 0x8

    int-to-long v12, v10

    or-long/2addr v8, v12

    aput-wide v8, v6, v5

    .line 69
    iget-object v6, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget-object v6, v6, Lcom/google/ctf/sandbox/o;->o:[J

    aget-wide v8, v6, v5

    mul-int/lit8 v10, v5, 0x4

    invoke-virtual {v3, v10}, Ljava/lang/String;->charAt(I)C

    move-result v10

    int-to-long v12, v10

    or-long/2addr v8, v12

    aput-wide v8, v6, v5

    .line 65
    add-int/lit8 v5, v5, 0x1

    goto :goto_4

    .line 72
    .end local v5    # "i":I
    :cond_3
    const-wide v4, 0x100000000L

    .line 73
    .local v4, "m":J
    iget-object v6, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget-object v7, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget-object v7, v7, Lcom/google/ctf/sandbox/o;->o:[J

    iget-object v8, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget v8, v8, Lcom/google/ctf/sandbox/o;->o:I

    aget-wide v8, v7, v8

    invoke-static {v8, v9, v4, v5}, Lcom/google/ctf/sandbox/R;->o(JJ)[J

    move-result-object v6

    .line 74
    .local v6, "g":[J
    const/4 v7, 0x0

    aget-wide v7, v6, v7

    rem-long/2addr v7, v4

    add-long/2addr v7, v4

    rem-long/2addr v7, v4

    .line 75
    .local v7, "inv":J
    iget-object v9, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget-object v9, v9, Lcom/google/ctf/sandbox/o;->class:[J

    iget-object v10, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget v10, v10, Lcom/google/ctf/sandbox/o;->o:I

    aget-wide v10, v9, v10

    cmp-long v9, v7, v10

    if-eqz v9, :cond_4

    .line 76
    iget-object v9, v1, Lcom/google/ctf/sandbox/o$1;->val$textView:Landroid/widget/TextView;

    const-string v10, "\u274c"

    invoke-virtual {v9, v10}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 77
    return-void

    .line 79
    :cond_4
    iget-object v9, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget v10, v9, Lcom/google/ctf/sandbox/o;->o:I

    const/4 v11, 0x1

    add-int/2addr v10, v11

    iput v10, v9, Lcom/google/ctf/sandbox/o;->o:I

    .line 81
    iget-object v9, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget v9, v9, Lcom/google/ctf/sandbox/o;->o:I

    iget-object v10, v1, Lcom/google/ctf/sandbox/o$1;->this$0:Lcom/google/ctf/sandbox/o;

    iget-object v10, v10, Lcom/google/ctf/sandbox/o;->o:[J

    array-length v10, v10

    if-lt v9, v10, :cond_5

    .line 82
    iget-object v9, v1, Lcom/google/ctf/sandbox/o$1;->val$textView:Landroid/widget/TextView;

    const-string v10, "\ud83d\udea9"

    invoke-virtual {v9, v10}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V

    .line 83
    return-void

    .line 86
    .end local v2    # "e":Ljava/lang/Exception;
    .end local v3    # "flagString":Ljava/lang/String;
    .end local v4    # "m":J
    .end local v6    # "g":[J
    .end local v7    # "inv":J
    :cond_5
    new-instance v8, Ljava/lang/RuntimeException;

    invoke-direct {v8}, Ljava/lang/RuntimeException;-><init>()V

    throw v8

    :goto_5
    return-void

    nop

    .array-data 8
        0x1
    .end array-data
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0
.end method
