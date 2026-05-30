
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

00000000004056bd <.text+0x458d>:
  4056bd:	f3 0f 1e fa          	endbr64 
  4056c1:	55                   	push   rbp
  4056c2:	48 89 e5             	mov    rbp,rsp
  4056c5:	48 83 ec 60          	sub    rsp,0x60
  4056c9:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  4056cd:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  4056d4:	00 00 
  4056d6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  4056da:	31 c0                	xor    eax,eax
  4056dc:	c7 45 b4 4f 10 00 00 	mov    DWORD PTR [rbp-0x4c],0x104f
  4056e3:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  4056e6:	35 2f ff ff ff       	xor    eax,0xffffff2f
  4056eb:	89 c2                	mov    edx,eax
  4056ed:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  4056f0:	24 2f                	and    al,0x2f
  4056f2:	01 c0                	add    eax,eax
  4056f4:	01 d0                	add    eax,edx
  4056f6:	83 c0 01             	add    eax,0x1
  4056f9:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  4056fc:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  4056ff:	34 e8                	xor    al,0xe8
  405701:	89 c2                	mov    edx,eax
  405703:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  405706:	25 e8 00 00 00       	and    eax,0xe8
  40570b:	01 c0                	add    eax,eax
  40570d:	01 d0                	add    eax,edx
  40570f:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  405712:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  405715:	34 bc                	xor    al,0xbc
  405717:	89 c2                	mov    edx,eax
  405719:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  40571c:	25 bc 00 00 00       	and    eax,0xbc
  405721:	01 c0                	add    eax,eax
  405723:	01 d0                	add    eax,edx
  405725:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  405728:	48 b8 51 6b 70 2e 22 	movabs rax,0x6b6a76222e706b51
  40572f:	76 6a 6b 
  405732:	48 ba 71 22 6b 71 22 	movabs rdx,0x55226322716b2271
  405739:	63 22 55 
  40573c:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  405740:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  405744:	48 b8 55 67 6c 66 7b 	movabs rax,0x2c71257b666c6755
  40574b:	25 71 2c 
  40574e:	48 89 45 cf          	mov    QWORD PTR [rbp-0x31],rax
  405752:	c7 45 b8 00 00 00 00 	mov    DWORD PTR [rbp-0x48],0x0
  405759:	eb 30                	jmp    40578b <stderr@GLIBC_2.2.5-0x4a895>
  40575b:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40575e:	48 98                	cdqe   
  405760:	0f b6 54 05 c0       	movzx  edx,BYTE PTR [rbp+rax*1-0x40]
  405765:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  405768:	48 98                	cdqe   
  40576a:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  40576f:	83 e0 02             	and    eax,0x2
  405772:	8d 0c 00             	lea    ecx,[rax+rax*1]
  405775:	89 d0                	mov    eax,edx
  405777:	29 c8                	sub    eax,ecx
  405779:	83 c0 02             	add    eax,0x2
  40577c:	89 c2                	mov    edx,eax
  40577e:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  405781:	48 98                	cdqe   
  405783:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  405787:	83 45 b8 01          	add    DWORD PTR [rbp-0x48],0x1
  40578b:	83 7d b8 16          	cmp    DWORD PTR [rbp-0x48],0x16
  40578f:	7e ca                	jle    40575b <stderr@GLIBC_2.2.5-0x4a8c5>
  405791:	c6 45 f7 00          	mov    BYTE PTR [rbp-0x9],0x0
  405795:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
  405799:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  40579c:	0f be c0             	movsx  eax,al
  40579f:	83 c0 0a             	add    eax,0xa
  4057a2:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
  4057a5:	eb 3c                	jmp    4057e3 <stderr@GLIBC_2.2.5-0x4a83d>
  4057a7:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  4057aa:	83 e0 01             	and    eax,0x1
  4057ad:	85 c0                	test   eax,eax
  4057af:	75 07                	jne    4057b8 <stderr@GLIBC_2.2.5-0x4a868>
  4057b1:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  4057b4:	d1 e8                	shr    eax,1
  4057b6:	eb 21                	jmp    4057d9 <stderr@GLIBC_2.2.5-0x4a847>
  4057b8:	8b 55 bc             	mov    edx,DWORD PTR [rbp-0x44]
  4057bb:	89 d0                	mov    eax,edx
  4057bd:	01 c0                	add    eax,eax
  4057bf:	01 d0                	add    eax,edx
  4057c1:	83 f0 fe             	xor    eax,0xfffffffe
  4057c4:	89 c1                	mov    ecx,eax
  4057c6:	8b 55 bc             	mov    edx,DWORD PTR [rbp-0x44]
  4057c9:	89 d0                	mov    eax,edx
  4057cb:	01 c0                	add    eax,eax
  4057cd:	01 d0                	add    eax,edx
  4057cf:	83 e0 fe             	and    eax,0xfffffffe
  4057d2:	01 c0                	add    eax,eax
  4057d4:	01 c8                	add    eax,ecx
  4057d6:	83 c0 01             	add    eax,0x1
  4057d9:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
  4057dc:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  4057df:	85 c0                	test   eax,eax
  4057e1:	74 08                	je     4057eb <stderr@GLIBC_2.2.5-0x4a835>
  4057e3:	83 7d bc 01          	cmp    DWORD PTR [rbp-0x44],0x1
  4057e7:	75 be                	jne    4057a7 <stderr@GLIBC_2.2.5-0x4a879>
  4057e9:	eb 01                	jmp    4057ec <stderr@GLIBC_2.2.5-0x4a834>
  4057eb:	90                   	nop
  4057ec:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  4057f0:	48 89 c7             	mov    rdi,rax
  4057f3:	e8 b8 b8 ff ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  4057f8:	bf 01 00 00 00       	mov    edi,0x1
  4057fd:	e8 0e b9 ff ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  405802:	f3 0f 1e fa          	endbr64 
  405806:	55                   	push   rbp
  405807:	48 89 e5             	mov    rbp,rsp
  40580a:	48 83 ec 70          	sub    rsp,0x70
  40580e:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  405812:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  405819:	00 00 
  40581b:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  40581f:	31 c0                	xor    eax,eax
  405821:	c7 45 a0 59 51 00 00 	mov    DWORD PTR [rbp-0x60],0x5159
  405828:	8b 45 a0             	mov    eax,DWORD PTR [rbp-0x60]
  40582b:	83 f0 32             	xor    eax,0x32
  40582e:	89 c2                	mov    edx,eax
  405830:	8b 45 a0             	mov    eax,DWORD PTR [rbp-0x60]
  405833:	83 e0 32             	and    eax,0x32
  405836:	01 c0                	add    eax,eax
  405838:	01 d0                	add    eax,edx
  40583a:	89 45 a0             	mov    DWORD PTR [rbp-0x60],eax
  40583d:	8b 45 a0             	mov    eax,DWORD PTR [rbp-0x60]
  405840:	83 f0 a2             	xor    eax,0xffffffa2
  405843:	89 c2                	mov    edx,eax
  405845:	8b 45 a0             	mov    eax,DWORD PTR [rbp-0x60]
  405848:	83 e0 a2             	and    eax,0xffffffa2
  40584b:	01 c0                	add    eax,eax
  40584d:	01 d0                	add    eax,edx
  40584f:	83 c0 01             	add    eax,0x1
  405852:	89 45 a0             	mov    DWORD PTR [rbp-0x60],eax
  405855:	8b 55 a0             	mov    edx,DWORD PTR [rbp-0x60]
  405858:	8b 45 a0             	mov    eax,DWORD PTR [rbp-0x60]
  40585b:	25 a6 00 00 00       	and    eax,0xa6
  405860:	01 c0                	add    eax,eax
  405862:	29 c2                	sub    edx,eax
  405864:	8d 82 a6 00 00 00    	lea    eax,[rdx+0xa6]
  40586a:	89 45 a0             	mov    DWORD PTR [rbp-0x60],eax
  40586d:	8b 45 a0             	mov    eax,DWORD PTR [rbp-0x60]
  405870:	0c fc                	or     al,0xfc
  405872:	89 c1                	mov    ecx,eax
  405874:	8b 45 a0             	mov    eax,DWORD PTR [rbp-0x60]
  405877:	25 fc 00 00 00       	and    eax,0xfc
  40587c:	89 c2                	mov    edx,eax
  40587e:	89 c8                	mov    eax,ecx
  405880:	29 d0                	sub    eax,edx
  405882:	89 45 a0             	mov    DWORD PTR [rbp-0x60],eax
  405885:	48 b8 cf e2 ef ab f2 	movabs rax,0xabfee4f2abefe2cf
  40588c:	e4 fe ab 
  40588f:	48 ba e6 ee ea e5 ab 	movabs rdx,0xabe4ffabe5eaeee6
  405896:	ff e4 ab 
  405899:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  40589d:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  4058a1:	48 b8 ef e4 ab ff e3 	movabs rax,0xb4ffeae3ffabe4ef
  4058a8:	ea ff b4 
  4058ab:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  4058af:	c7 45 a4 00 00 00 00 	mov    DWORD PTR [rbp-0x5c],0x0
  4058b6:	eb 1c                	jmp    4058d4 <stderr@GLIBC_2.2.5-0x4a74c>
  4058b8:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4058bb:	48 98                	cdqe   
  4058bd:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  4058c2:	83 f0 8b             	xor    eax,0xffffff8b
  4058c5:	89 c2                	mov    edx,eax
  4058c7:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4058ca:	48 98                	cdqe   
  4058cc:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  4058d0:	83 45 a4 01          	add    DWORD PTR [rbp-0x5c],0x1
  4058d4:	83 7d a4 17          	cmp    DWORD PTR [rbp-0x5c],0x17
  4058d8:	7e de                	jle    4058b8 <stderr@GLIBC_2.2.5-0x4a768>
  4058da:	c6                   	.byte 0xc6
  4058db:	45                   	rex.RB
  4058dc:	e8                   	.byte 0xe8
