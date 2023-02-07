

# TP2 de Dembélé Alex

`pandoc -s --toc tp2.md --css=./github-pandoc.css -o tp1.html`





## lscpu

```
Architecture :                              x86_64
  Mode(s) opératoire(s) des processeurs :   32-bit, 64-bit
  Address sizes:                            39 bits physical, 48 bits virtual
  Boutisme :                                Little Endian
Processeur(s) :                             8
  Liste de processeur(s) en ligne :         0-7
Identifiant constructeur :                  GenuineIntel
  Nom de modèle :                           11th Gen Intel(R) Core(TM) i7-1165G7
                                             @ 2.80GHz
    Famille de processeur :                 6
    Modèle :                                140
    Thread(s) par cœur :                    2
    Cœur(s) par socket :                    4
    Socket(s) :                             1
    Révision :                              1
    Vitesse maximale du processeur en MHz : 4700,0000
    Vitesse minimale du processeur en MHz : 400,0000
    BogoMIPS :                              5606.40
    Drapaux :                               fpu vme de pse tsc msr pae mce cx8 a
                                            pic sep mtrr pge mca cmov pat pse36 
                                            clflush dts acpi mmx fxsr sse sse2 s
                                            s ht tm pbe syscall nx pdpe1gb rdtsc
                                            p lm constant_tsc art arch_perfmon p
                                            ebs bts rep_good nopl xtopology nons
                                            top_tsc cpuid aperfmperf tsc_known_f
                                            req pni pclmulqdq dtes64 monitor ds_
                                            cpl vmx est tm2 ssse3 sdbg fma cx16 
                                            xtpr pdcm pcid sse4_1 sse4_2 x2apic 
                                            movbe popcnt tsc_deadline_timer aes 
                                            xsave avx f16c rdrand lahf_lm abm 3d
                                            nowprefetch cpuid_fault epb cat_l2 i
                                            nvpcid_single cdp_l2 ssbd ibrs ibpb 
                                            stibp ibrs_enhanced tpr_shadow vnmi 
                                            flexpriority ept vpid ept_ad fsgsbas
                                            e tsc_adjust bmi1 avx2 smep bmi2 erm
                                            s invpcid rdt_a avx512f avx512dq rds
                                            eed adx smap avx512ifma clflushopt c
                                            lwb intel_pt avx512cd sha_ni avx512b
                                            w avx512vl xsaveopt xsavec xgetbv1 x
                                            saves split_lock_detect dtherm ida a
                                            rat pln pts hwp hwp_notify hwp_act_w
                                            indow hwp_epp hwp_pkg_req avx512vbmi
                                             umip pku ospke avx512_vbmi2 gfni va
                                            es vpclmulqdq avx512_vnni avx512_bit
                                            alg avx512_vpopcntdq rdpid movdiri m
                                            ovdir64b fsrm avx512_vp2intersect md
                                            _clear flush_l1d arch_capabilities
Virtualization features:                    
  Virtualisation :                          VT-x
Caches (sum of all):                        
  L1d:                                      192 KiB (4 instances)
  L1i:                                      128 KiB (4 instances)
  L2:                                       5 MiB (4 instances)
  L3:                                       12 MiB (1 instance)
NUMA:                                       
  Nœud(s) NUMA :                            1
  Nœud NUMA 0 de processeur(s) :            0-7
Vulnerabilities:                            
  Itlb multihit:                            Not affected
  L1tf:                                     Not affected
  Mds:                                      Not affected
  Meltdown:                                 Not affected
  Mmio stale data:                          Not affected
  Retbleed:                                 Not affected
  Spec store bypass:                        Mitigation; Speculative Store Bypass
                                             disabled via prctl and seccomp
  Spectre v1:                               Mitigation; usercopy/swapgs barriers
                                             and __user pointer sanitization
  Spectre v2:                               Mitigation; Enhanced IBRS, IBPB cond
                                            itional, RSB filling, PBRSB-eIBRS SW
                                             sequence
  Srbds:                                    Not affected
  Tsx async abort:                          Not affected

```

*Des infos utiles s'y trouvent : nb core, taille de cache*



## Produit matrice-matrice



### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :* MAKE ALL

`make TestProduct.exe && ./TestProduct.exe 1024`


  ordre           | time    | MFlops  | MFlops(n=2048) 
------------------|---------|---------|----------------
i,j,k (origine)   | 2.73764 | 782.476 |                
j,i,k             | 2.3068  | 930.937 |    
i,k,j             | 4.45192 | 482.373 |    
k,i,j             | 4.94135 | 434.595 |    
j,k,i             | 0.480267 | 4471.44 | 3206.25   
k,j,i             | 0.525439 | 4087.03 | 3015.12  


Selon l'ordre, il y a des énormes différences. 
L’ex ́ecution est pus rapide en mettant la boucle en i `a la fin, car on utilise de la m ́emoire cache. Les
C(i,j) sont dans le cache et il n’y a pas besoin de les rechercher `a chaque fois dans la m ́emoire. De
plus, les matrices sont stock ́es par colonne, donc les coeff A(i,k) sont les plus coˆuteux `a chercher. LEs
A(i,k) sont bien g ́er ́e par le cache lorsque la boucle en i est la plus interne



### OMP sur la meilleure boucle 

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
1                 |13987.3| 12272.2          |10316.4         |11905.7
2                 | 12396.2 |12396.2         |12396.2           |12146.5
3                 |  |
4                 |  |
5                 |  |
6                 |  |
7                 |  |
8                 | 14053.2 | 12302.1        |7251.43         |12076.8




### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024` Num thread=4 + OMP

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    |  |
32                |  5136.17|5099.58|3702.73
64                | 8324.46 | 12926.1|7837.54
128               | 14596.5 |13568.2|8134.44
256               |  14610.3|13576| Failed
512               |  | 13529.7|4373.08
1024              |4421.6  ||4445.73




### Bloc + OMP



  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|-------------------------------------------------|
A.nbCols       |  1      |   4272.78      |                |                |               |
128           |  8      |14664.2    |                |                |               |
---------------|---------|---------|-------------------------------------------------|
Speed-up       |         |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|



### Comparaison with BLAS


# Tips 

```
	env 
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
