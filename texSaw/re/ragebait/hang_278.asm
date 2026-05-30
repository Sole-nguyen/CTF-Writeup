
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

0000000000413757 <.text+0x12627>:
  413757:	f3 0f 1e fa          	endbr64 
  41375b:	55                   	push   rbp
  41375c:	48 89 e5             	mov    rbp,rsp
  41375f:	48 83 ec 70          	sub    rsp,0x70
  413763:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  413767:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  41376e:	00 00 
  413770:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  413774:	31 c0                	xor    eax,eax
  413776:	c7 45 a4 49 01 00 00 	mov    DWORD PTR [rbp-0x5c],0x149
  41377d:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  413780:	83 f0 81             	xor    eax,0xffffff81
  413783:	89 c2                	mov    edx,eax
  413785:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  413788:	83 e0 81             	and    eax,0xffffff81
  41378b:	01 c0                	add    eax,eax
  41378d:	01 d0                	add    eax,edx
  41378f:	83 c0 01             	add    eax,0x1
  413792:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  413795:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  413798:	83 f0 d2             	xor    eax,0xffffffd2
  41379b:	89 c2                	mov    edx,eax
  41379d:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4137a0:	83 e0 d2             	and    eax,0xffffffd2
  4137a3:	01 c0                	add    eax,eax
  4137a5:	01 d0                	add    eax,edx
  4137a7:	83 c0 01             	add    eax,0x1
  4137aa:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4137ad:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4137b0:	35 71 ff ff ff       	xor    eax,0xffffff71
  4137b5:	89 c2                	mov    edx,eax
  4137b7:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4137ba:	24 71                	and    al,0x71
  4137bc:	01 c0                	add    eax,eax
  4137be:	01 d0                	add    eax,edx
  4137c0:	83 c0 01             	add    eax,0x1
  4137c3:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4137c6:	48 b8 7b 46 15 41 12 	movabs rax,0x465d5c124115467b
  4137cd:	5c 5d 46 
  4137d0:	48 ba 12 53 12 50 47 	movabs rdx,0x121e554750125312
  4137d7:	55 1e 12 
  4137da:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  4137de:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  4137e2:	48 b8 12 5b 46 15 41 	movabs rax,0x1253124115465b12
  4137e9:	12 53 12 
  4137ec:	48 ba 54 57 53 46 47 	movabs rdx,0x1357404746535754
  4137f3:	40 57 13 
  4137f6:	48 89 45 bf          	mov    QWORD PTR [rbp-0x41],rax
  4137fa:	48 89 55 c7          	mov    QWORD PTR [rbp-0x39],rdx
  4137fe:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  413805:	eb 30                	jmp    413837 <stderr@GLIBC_2.2.5-0x3c7e9>
  413807:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  41380a:	48 98                	cdqe   
  41380c:	0f b6 54 05 b0       	movzx  edx,BYTE PTR [rbp+rax*1-0x50]
  413811:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  413814:	48 98                	cdqe   
  413816:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  41381b:	83 e0 32             	and    eax,0x32
  41381e:	8d 0c 00             	lea    ecx,[rax+rax*1]
  413821:	89 d0                	mov    eax,edx
  413823:	29 c8                	sub    eax,ecx
  413825:	83 c0 32             	add    eax,0x32
  413828:	89 c2                	mov    edx,eax
  41382a:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  41382d:	48 98                	cdqe   
  41382f:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  413833:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  413837:	83 7d a8 1e          	cmp    DWORD PTR [rbp-0x58],0x1e
  41383b:	7e ca                	jle    413807 <stderr@GLIBC_2.2.5-0x3c819>
  41383d:	c6 45 ef 00          	mov    BYTE PTR [rbp-0x11],0x0
  413841:	c7 45 ac 00 00 00 00 	mov    DWORD PTR [rbp-0x54],0x0
  413848:	eb 19                	jmp    413863 <stderr@GLIBC_2.2.5-0x3c7bd>
  41384a:	8b 55 a4             	mov    edx,DWORD PTR [rbp-0x5c]
  41384d:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  413850:	31 d0                	xor    eax,edx
  413852:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  413855:	bf 64 00 00 00       	mov    edi,0x64
  41385a:	e8 c1 d8 fe ff       	call   401120 <stderr@GLIBC_2.2.5-0x4ef00>
  41385f:	83 45 ac 01          	add    DWORD PTR [rbp-0x54],0x1
  413863:	81 7d ac 53 12 00 00 	cmp    DWORD PTR [rbp-0x54],0x1253
  41386a:	7e de                	jle    41384a <stderr@GLIBC_2.2.5-0x3c7d6>
  41386c:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  413870:	48 89 c7             	mov    rdi,rax
  413873:	e8 38 d8 fe ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  413878:	bf 01 00 00 00       	mov    edi,0x1
  41387d:	e8 8e d8 fe ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  413882:	f3 0f 1e fa          	endbr64 
  413886:	55                   	push   rbp
  413887:	48 89 e5             	mov    rbp,rsp
  41388a:	48 83 ec 70          	sub    rsp,0x70
  41388e:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  413892:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  413899:	00 00 
  41389b:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  41389f:	31 c0                	xor    eax,eax
  4138a1:	c7 45 a4 1d b0 00 00 	mov    DWORD PTR [rbp-0x5c],0xb01d
  4138a8:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4138ab:	83 f0 c5             	xor    eax,0xffffffc5
  4138ae:	89 c2                	mov    edx,eax
  4138b0:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4138b3:	83 e0 c5             	and    eax,0xffffffc5
  4138b6:	01 c0                	add    eax,eax
  4138b8:	01 d0                	add    eax,edx
  4138ba:	83 c0 01             	add    eax,0x1
  4138bd:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4138c0:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4138c3:	0c 90                	or     al,0x90
  4138c5:	89 c2                	mov    edx,eax
  4138c7:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4138ca:	25 90 00 00 00       	and    eax,0x90
  4138cf:	01 d0                	add    eax,edx
  4138d1:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4138d4:	8b 55 a4             	mov    edx,DWORD PTR [rbp-0x5c]
  4138d7:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4138da:	25 ac 00 00 00       	and    eax,0xac
  4138df:	01 c0                	add    eax,eax
  4138e1:	29 c2                	sub    edx,eax
  4138e3:	8d 82 ac 00 00 00    	lea    eax,[rdx+0xac]
  4138e9:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4138ec:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4138ef:	83 f0 82             	xor    eax,0xffffff82
  4138f2:	89 c2                	mov    edx,eax
  4138f4:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4138f7:	83 e0 82             	and    eax,0xffffff82
  4138fa:	01 c0                	add    eax,eax
  4138fc:	01 d0                	add    eax,edx
  4138fe:	83 c0 01             	add    eax,0x1
  413901:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  413904:	48 b8 8b be ac b4 ff 	movabs rax,0xb6beb9ffb4acbe8b
  41390b:	b9 be b6 
  41390e:	48 ba b3 ba bb ff ac 	movabs rdx,0xbcbcaaacffbbbab3
  413915:	aa bc bc 
  413918:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  41391c:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  413920:	48 b8 ba bb ff ac aa 	movabs rax,0xbabcbcaaacffbbba
  413927:	bc bc ba 
  41392a:	48 ba ac ac b9 aa b3 	movabs rdx,0xf1a6b3b3aab9acac
  413931:	b3 a6 f1 
  413934:	48 89 45 b9          	mov    QWORD PTR [rbp-0x47],rax
  413938:	48 89 55 c1          	mov    QWORD PTR [rbp-0x3f],rdx
  41393c:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  413943:	eb 1c                	jmp    413961 <stderr@GLIBC_2.2.5-0x3c6bf>
  413945:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  413948:	48 98                	cdqe   
  41394a:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  41394f:	83 f0 df             	xor    eax,0xffffffdf
  413952:	89 c2                	mov    edx,eax
  413954:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  413957:	48 98                	cdqe   
  413959:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  41395d:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  413961:	83 7d a8 18          	cmp    DWORD PTR [rbp-0x58],0x18
  413965:	7e de                	jle    413945 <stderr@GLIBC_2.2.5-0x3c6db>
  413967:	c6 45 e9 00          	mov    BYTE PTR [rbp-0x17],0x0
  41396b:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
  41396f:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  413972:	0f be c0             	movsx  eax,al
  413975:	83                   	.byte 0x83
  413976:	c0                   	.byte 0xc0
