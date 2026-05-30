
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

000000000040b8ae <.text+0xa77e>:
  40b8ae:	f3 0f 1e fa          	endbr64 
  40b8b2:	55                   	push   rbp
  40b8b3:	48 89 e5             	mov    rbp,rsp
  40b8b6:	48 83 ec 70          	sub    rsp,0x70
  40b8ba:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  40b8be:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  40b8c5:	00 00 
  40b8c7:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  40b8cb:	31 c0                	xor    eax,eax
  40b8cd:	c7 45 a4 ba 74 00 00 	mov    DWORD PTR [rbp-0x5c],0x74ba
  40b8d4:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40b8d7:	83 f0 b2             	xor    eax,0xffffffb2
  40b8da:	89 c2                	mov    edx,eax
  40b8dc:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40b8df:	83 e0 b2             	and    eax,0xffffffb2
  40b8e2:	01 c0                	add    eax,eax
  40b8e4:	01 d0                	add    eax,edx
  40b8e6:	83 c0 01             	add    eax,0x1
  40b8e9:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  40b8ec:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40b8ef:	83 c8 66             	or     eax,0x66
  40b8f2:	89 c2                	mov    edx,eax
  40b8f4:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40b8f7:	83 e0 66             	and    eax,0x66
  40b8fa:	01 d0                	add    eax,edx
  40b8fc:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  40b8ff:	8b 55 a4             	mov    edx,DWORD PTR [rbp-0x5c]
  40b902:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40b905:	83 e0 56             	and    eax,0x56
  40b908:	01 c0                	add    eax,eax
  40b90a:	29 c2                	sub    edx,eax
  40b90c:	8d 42 56             	lea    eax,[rdx+0x56]
  40b90f:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  40b912:	48 b8 b4 89 da 8e dd 	movabs rax,0x899293dd8eda89b4
  40b919:	93 92 89 
  40b91c:	48 ba dd 9c dd 9f 88 	movabs rdx,0xddd19a889fdd9cdd
  40b923:	9a d1 dd 
  40b926:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  40b92a:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  40b92e:	48 b8 dd 94 89 da 8e 	movabs rax,0xdd9cdd8eda8994dd
  40b935:	dd 9c dd 
  40b938:	48 ba 9b 98 9c 89 88 	movabs rdx,0xdc988f88899c989b
  40b93f:	8f 98 dc 
  40b942:	48 89 45 bf          	mov    QWORD PTR [rbp-0x41],rax
  40b946:	48 89 55 c7          	mov    QWORD PTR [rbp-0x39],rdx
  40b94a:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  40b951:	eb 31                	jmp    40b984 <stderr@GLIBC_2.2.5-0x4469c>
  40b953:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  40b956:	48 98                	cdqe   
  40b958:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  40b95d:	83 c8 fd             	or     eax,0xfffffffd
  40b960:	89 c2                	mov    edx,eax
  40b962:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  40b965:	48 98                	cdqe   
  40b967:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  40b96c:	83 e0 fd             	and    eax,0xfffffffd
  40b96f:	89 c1                	mov    ecx,eax
  40b971:	89 d0                	mov    eax,edx
  40b973:	29 c8                	sub    eax,ecx
  40b975:	89 c2                	mov    edx,eax
  40b977:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  40b97a:	48 98                	cdqe   
  40b97c:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  40b980:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  40b984:	83 7d a8 1e          	cmp    DWORD PTR [rbp-0x58],0x1e
  40b988:	7e c9                	jle    40b953 <stderr@GLIBC_2.2.5-0x446cd>
  40b98a:	c6 45 ef 00          	mov    BYTE PTR [rbp-0x11],0x0
  40b98e:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
  40b992:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  40b995:	0f be c0             	movsx  eax,al
  40b998:	83 c0 05             	add    eax,0x5
  40b99b:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  40b99e:	eb 3c                	jmp    40b9dc <stderr@GLIBC_2.2.5-0x44644>
  40b9a0:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  40b9a3:	83 e0 01             	and    eax,0x1
  40b9a6:	85 c0                	test   eax,eax
  40b9a8:	75 07                	jne    40b9b1 <stderr@GLIBC_2.2.5-0x4466f>
  40b9aa:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  40b9ad:	d1 e8                	shr    eax,1
  40b9af:	eb 21                	jmp    40b9d2 <stderr@GLIBC_2.2.5-0x4464e>
  40b9b1:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  40b9b4:	89 d0                	mov    eax,edx
  40b9b6:	01 c0                	add    eax,eax
  40b9b8:	01 d0                	add    eax,edx
  40b9ba:	83 f0 fe             	xor    eax,0xfffffffe
  40b9bd:	89 c1                	mov    ecx,eax
  40b9bf:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  40b9c2:	89 d0                	mov    eax,edx
  40b9c4:	01 c0                	add    eax,eax
  40b9c6:	01 d0                	add    eax,edx
  40b9c8:	83 e0 fe             	and    eax,0xfffffffe
  40b9cb:	01 c0                	add    eax,eax
  40b9cd:	01 c8                	add    eax,ecx
  40b9cf:	83 c0 01             	add    eax,0x1
  40b9d2:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  40b9d5:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40b9d8:	85 c0                	test   eax,eax
  40b9da:	74 08                	je     40b9e4 <stderr@GLIBC_2.2.5-0x4463c>
  40b9dc:	83 7d ac 01          	cmp    DWORD PTR [rbp-0x54],0x1
  40b9e0:	75 be                	jne    40b9a0 <stderr@GLIBC_2.2.5-0x44680>
  40b9e2:	eb 01                	jmp    40b9e5 <stderr@GLIBC_2.2.5-0x4463b>
  40b9e4:	90                   	nop
  40b9e5:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  40b9e9:	48 89 c7             	mov    rdi,rax
  40b9ec:	e8 bf 56 ff ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  40b9f1:	bf 01 00 00 00       	mov    edi,0x1
  40b9f6:	e8 15 57 ff ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  40b9fb:	f3 0f 1e fa          	endbr64 
  40b9ff:	55                   	push   rbp
  40ba00:	48 89 e5             	mov    rbp,rsp
  40ba03:	48 83 ec 60          	sub    rsp,0x60
  40ba07:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  40ba0b:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  40ba12:	00 00 
  40ba14:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  40ba18:	31 c0                	xor    eax,eax
  40ba1a:	c7 45 b8 27 ea 00 00 	mov    DWORD PTR [rbp-0x48],0xea27
  40ba21:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40ba24:	83 c8 26             	or     eax,0x26
  40ba27:	89 c1                	mov    ecx,eax
  40ba29:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40ba2c:	83 e0 26             	and    eax,0x26
  40ba2f:	89 c2                	mov    edx,eax
  40ba31:	89 c8                	mov    eax,ecx
  40ba33:	29 d0                	sub    eax,edx
  40ba35:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40ba38:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40ba3b:	83 c8 72             	or     eax,0x72
  40ba3e:	89 c2                	mov    edx,eax
  40ba40:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40ba43:	83 e0 72             	and    eax,0x72
  40ba46:	01 d0                	add    eax,edx
  40ba48:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40ba4b:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40ba4e:	83 c8 39             	or     eax,0x39
  40ba51:	89 c2                	mov    edx,eax
  40ba53:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40ba56:	83 e0 39             	and    eax,0x39
  40ba59:	01 d0                	add    eax,edx
  40ba5b:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40ba5e:	48 b8 f3 c9 d2 8c 80 	movabs rax,0xc9c8d4808cd2c9f3
  40ba65:	d4 c8 c9 
  40ba68:	48 ba d3 80 c9 d3 80 	movabs rdx,0xf780c180d3c980d3
  40ba6f:	c1 80 f7 
  40ba72:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  40ba76:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  40ba7a:	48 b8 f7 c5 ce c4 d9 	movabs rax,0x8ed387d9c4cec5f7
  40ba81:	87 d3 8e 
  40ba84:	48 89 45 cf          	mov    QWORD PTR [rbp-0x31],rax
  40ba88:	c7 45 bc 00 00 00 00 	mov    DWORD PTR [rbp-0x44],0x0
  40ba8f:	eb 30                	jmp    40bac1 <stderr@GLIBC_2.2.5-0x4455f>
  40ba91:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40ba94:	48 98                	cdqe   
  40ba96:	0f b6 54 05 c0       	movzx  edx,BYTE PTR [rbp+rax*1-0x40]
  40ba9b:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40ba9e:	48 98                	cdqe   
  40baa0:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  40baa5:	83 e0 a0             	and    eax,0xffffffa0
  40baa8:	8d 0c 00             	lea    ecx,[rax+rax*1]
  40baab:	89 d0                	mov    eax,edx
  40baad:	29 c8                	sub    eax,ecx
  40baaf:	83 e8 60             	sub    eax,0x60
  40bab2:	89 c2                	mov    edx,eax
  40bab4:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40bab7:	48 98                	cdqe   
  40bab9:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  40babd:	83 45 bc 01          	add    DWORD PTR [rbp-0x44],0x1
  40bac1:	83 7d bc 16          	cmp    DWORD PTR [rbp-0x44],0x16
  40bac5:	7e ca                	jle    40ba91 <stderr@GLIBC_2.2.5-0x4458f>
  40bac7:	c6 45 f7 00          	mov    BYTE PTR [rbp-0x9],0x0
  40bacb:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
