# gboad maddy

## Description
<pre>
You see this everyday if you use android.

?<³|⁰([{⁰|%f¹&<=f{³&f"{%)

Author : Finch
</pre>
## Hint
```
len(flag)=28
```

Someone pointed out after the ctf  
> They we small accent symbols on gboard   
**HMMMMMMMMMMMMMMMMMMMMMM**

![](gboard.png)

Substituting the accent symbols for the letter, we can get

```
?<³|⁰([{⁰|%f¹&<=f{³&f"{%) 
mu3e0{to0eq_1gur_o3g_xoq}
```
rot13 of which produces  
```
zh3r0{gb0rd_1the_b3t_kbd}
```

Since the length of the flag was mentioned to be 28 characters, one has to fill out the possible missing characters :\

### zh3r0{gb0rd_1s_the_b3st_kbd}
