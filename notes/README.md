{% include mathjax.html %}

When \\(a \ne 0\\), there are two solutions to \\(ax^2 + bx + c = 0\\).

$$\left(\sum_{i=1}^{n}{\left|a_i\right|}^p\right)^{1/p}$$

# Breakdown of an ELF binary

* .interp
* .note.ABI-tag
* .note.gnu.build-id
* .gnu.hash
* .dynsym
* .dynstr
* .gnu.version
* .gnu.version_r
* .rela.dyn
* .rela.plt
* .init
* .plt
* .plt.got
* .text
* .fini
* .rodata
* .eh_frame_hdr
* .eh_frame
* .init_array
* .fini_array
* .jcr
* .dynamic
* .got
* .got.plt
* .data
* .bss

## .init
This holds the executable instructins that contribute to the process initialization code.  
When program starts run, it is executed before main program entry point

## .fini
Finish. Holds the executable instructions which will be executed after the `main` function returns

## .bss
Basic Service Set for statically-allocated variables that are not explicitly initialized to any value

### .sbss
Small bss for holding small statically-allocated data

## .data
Data segment, stores initialized static, global and static local variables
Both read and writeable section

## .init_array
Array of function pointers that contributes single initialization array for the executable or shared object containing section

## .fini_array
Array of function pointers that contributes to single termination array for executable or so containing the section

## .dynamic
Holds the dynamic linking information

## .dynstr
Strings for dynamic linking

## .dynsym
Dynamic linking symbol table

## .interp
Path name of program interpreter

## .line 
line number information for symbolic debugging

## .rodata
Ready only data for non-writable segment in process image

## .shstrtab
Holds section names

## .text
Holds the text or executable instructions of the program

## .ctors
list of global constructor function pointers

## .dtors
list of global destructor function pointers

## .eh_frame
exception handling frame information

## .eh_frame_hdr

<h2>An Identity of Ramanujan</h2>

<p>\[
   \frac{1}{(\sqrt{\phi \sqrt{5}}-\phi) e^{\frac25 \pi}} =
     1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {1+\frac{e^{-6\pi}}
      {1+\frac{e^{-8\pi}} {1+\ldots} } } }
\]</p>

[this link is useful](https://refspecs.linuxbase.org/LSB_3.0.0/LSB-PDA/LSB-PDA/specialsections.html)
