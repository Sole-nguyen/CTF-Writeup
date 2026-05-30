
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

0000000000415601 <.text+0x144d1>:
  415601:	f3 0f 1e fa          	endbr64 
  415605:	55                   	push   rbp
  415606:	48 89 e5             	mov    rbp,rsp
  415609:	48 83 ec 70          	sub    rsp,0x70
  41560d:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  415611:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  415618:	00 00 
  41561a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  41561e:	31 c0                	xor    eax,eax
  415620:	c7 45 a4 58 35 00 00 	mov    DWORD PTR [rbp-0x5c],0x3558
  415627:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  41562a:	83 c8 75             	or     eax,0x75
  41562d:	89 c1                	mov    ecx,eax
  41562f:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  415632:	83 e0 75             	and    eax,0x75
  415635:	89 c2                	mov    edx,eax
  415637:	89 c8                	mov    eax,ecx
  415639:	29 d0                	sub    eax,edx
  41563b:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  41563e:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  415641:	34 93                	xor    al,0x93
  415643:	89 c2                	mov    edx,eax
  415645:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  415648:	25 93 00 00 00       	and    eax,0x93
  41564d:	01 c0                	add    eax,eax
  41564f:	01 d0                	add    eax,edx
  415651:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  415654:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  415657:	83 f0 8d             	xor    eax,0xffffff8d
  41565a:	89 c2                	mov    edx,eax
  41565c:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  41565f:	83 e0 8d             	and    eax,0xffffff8d
  415662:	01 c0                	add    eax,eax
  415664:	01 d0                	add    eax,edx
  415666:	83 c0 01             	add    eax,0x1
  415669:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  41566c:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  41566f:	83 f0 e7             	xor    eax,0xffffffe7
  415672:	89 c2                	mov    edx,eax
  415674:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  415677:	83 e0 e7             	and    eax,0xffffffe7
  41567a:	01 c0                	add    eax,eax
  41567c:	01 d0                	add    eax,edx
  41567e:	83 c0 01             	add    eax,0x1
  415681:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  415684:	48 b8 67 4a 47 03 5a 	movabs rax,0x3564c5a03474a67
  41568b:	4c 56 03 
  41568e:	48 ba 4e 46 42 4d 03 	movabs rdx,0x34c57034d42464e
  415695:	57 4c 03 
  415698:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  41569c:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  4156a0:	48 b8 47 4c 03 57 4b 	movabs rax,0x1c57424b57034c47
  4156a7:	42 57 1c 
  4156aa:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  4156ae:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  4156b5:	eb 31                	jmp    4156e8 <stderr@GLIBC_2.2.5-0x3a938>
  4156b7:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  4156ba:	48 98                	cdqe   
  4156bc:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  4156c1:	83 c8 23             	or     eax,0x23
  4156c4:	89 c2                	mov    edx,eax
  4156c6:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  4156c9:	48 98                	cdqe   
  4156cb:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  4156d0:	83 e0 23             	and    eax,0x23
  4156d3:	89 c1                	mov    ecx,eax
  4156d5:	89 d0                	mov    eax,edx
  4156d7:	29 c8                	sub    eax,ecx
  4156d9:	89 c2                	mov    edx,eax
  4156db:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  4156de:	48 98                	cdqe   
  4156e0:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  4156e4:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  4156e8:	83 7d a8 17          	cmp    DWORD PTR [rbp-0x58],0x17
  4156ec:	7e c9                	jle    4156b7 <stderr@GLIBC_2.2.5-0x3a969>
  4156ee:	c6 45 e8 00          	mov    BYTE PTR [rbp-0x18],0x0
  4156f2:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
  4156f6:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  4156f9:	0f be c0             	movsx  eax,al
  4156fc:	83 c0 06             	add    eax,0x6
  4156ff:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  415702:	eb 3c                	jmp    415740 <stderr@GLIBC_2.2.5-0x3a8e0>
  415704:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  415707:	83 e0 01             	and    eax,0x1
  41570a:	85 c0                	test   eax,eax
  41570c:	75 07                	jne    415715 <stderr@GLIBC_2.2.5-0x3a90b>
  41570e:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  415711:	d1 e8                	shr    eax,1
  415713:	eb 21                	jmp    415736 <stderr@GLIBC_2.2.5-0x3a8ea>
  415715:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  415718:	89 d0                	mov    eax,edx
  41571a:	01 c0                	add    eax,eax
  41571c:	01 d0                	add    eax,edx
  41571e:	83 f0 fe             	xor    eax,0xfffffffe
  415721:	89 c1                	mov    ecx,eax
  415723:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  415726:	89 d0                	mov    eax,edx
  415728:	01 c0                	add    eax,eax
  41572a:	01 d0                	add    eax,edx
  41572c:	83 e0 fe             	and    eax,0xfffffffe
  41572f:	01 c0                	add    eax,eax
  415731:	01 c8                	add    eax,ecx
  415733:	83 c0 01             	add    eax,0x1
  415736:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  415739:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  41573c:	85 c0                	test   eax,eax
  41573e:	74 08                	je     415748 <stderr@GLIBC_2.2.5-0x3a8d8>
  415740:	83 7d ac 01          	cmp    DWORD PTR [rbp-0x54],0x1
  415744:	75 be                	jne    415704 <stderr@GLIBC_2.2.5-0x3a91c>
  415746:	eb 01                	jmp    415749 <stderr@GLIBC_2.2.5-0x3a8d7>
  415748:	90                   	nop
  415749:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  41574d:	48 89 c7             	mov    rdi,rax
  415750:	e8 5b b9 fe ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  415755:	bf 01 00 00 00       	mov    edi,0x1
  41575a:	e8 b1 b9 fe ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  41575f:	f3 0f 1e fa          	endbr64 
  415763:	55                   	push   rbp
  415764:	48 89 e5             	mov    rbp,rsp
  415767:	48 83 ec 60          	sub    rsp,0x60
  41576b:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  41576f:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  415776:	00 00 
  415778:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  41577c:	31 c0                	xor    eax,eax
  41577e:	c7 45 b4 2a 7d 00 00 	mov    DWORD PTR [rbp-0x4c],0x7d2a
  415785:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  415788:	83 c8 2a             	or     eax,0x2a
  41578b:	89 c1                	mov    ecx,eax
  41578d:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  415790:	83 e0 2a             	and    eax,0x2a
  415793:	89 c2                	mov    edx,eax
  415795:	89 c8                	mov    eax,ecx
  415797:	29 d0                	sub    eax,edx
  415799:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  41579c:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  41579f:	34 9c                	xor    al,0x9c
  4157a1:	89 c2                	mov    edx,eax
  4157a3:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  4157a6:	25 9c 00 00 00       	and    eax,0x9c
  4157ab:	01 c0                	add    eax,eax
  4157ad:	01 d0                	add    eax,edx
  4157af:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  4157b2:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  4157b5:	0c a9                	or     al,0xa9
  4157b7:	89 c1                	mov    ecx,eax
  4157b9:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  4157bc:	25 a9 00 00 00       	and    eax,0xa9
  4157c1:	89 c2                	mov    edx,eax
  4157c3:	89 c8                	mov    eax,ecx
  4157c5:	29 d0                	sub    eax,edx
  4157c7:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  4157ca:	48 b8 36 01 01 1c 01 	movabs rax,0x3f5349011c010136
  4157d1:	49 53 3f 
  4157d4:	48 ba 12 0a 16 01 53 	movabs rdx,0x3534b5301160a12
  4157db:	4b 53 03 
  4157de:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  4157e2:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  4157e6:	48 b8 03 01 1c 11 1f 	movabs rax,0x5d1e161f111c0103
  4157ed:	16 1e 5d 
  4157f0:	48 89 45 cf          	mov    QWORD PTR [rbp-0x31],rax
  4157f4:	c7 45 b8 00 00 00 00 	mov    DWORD PTR [rbp-0x48],0x0
  4157fb:	eb 1c                	jmp    415819 <stderr@GLIBC_2.2.5-0x3a807>
  4157fd:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  415800:	48 98                	cdqe   
  415802:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  415807:	83 f0 73             	xor    eax,0x73
  41580a:	89 c2                	mov    edx,eax
  41580c:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  41580f:	48 98                	cdqe   
  415811:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  415815:	83 45 b8 01          	add    DWORD PTR [rbp-0x48],0x1
  415819:	83 7d b8 16          	cmp    DWORD PTR [rbp-0x48],0x16
  41581d:	7e de                	jle    4157fd <stderr@GLIBC_2.2.5-0x3a823>
  41581f:	c6                   	.byte 0xc6
  415820:	45                   	rex.RB
