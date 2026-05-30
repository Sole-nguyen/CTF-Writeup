
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

000000000040c820 <.text+0xb6f0>:
  40c820:	f3 0f 1e fa          	endbr64 
  40c824:	55                   	push   rbp
  40c825:	48 89 e5             	mov    rbp,rsp
  40c828:	48 83 ec 60          	sub    rsp,0x60
  40c82c:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  40c830:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  40c837:	00 00 
  40c839:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  40c83d:	31 c0                	xor    eax,eax
  40c83f:	c7 45 b4 e8 19 00 00 	mov    DWORD PTR [rbp-0x4c],0x19e8
  40c846:	8b 55 b4             	mov    edx,DWORD PTR [rbp-0x4c]
  40c849:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  40c84c:	83 e0 6b             	and    eax,0x6b
  40c84f:	01 c0                	add    eax,eax
  40c851:	29 c2                	sub    edx,eax
  40c853:	8d 42 6b             	lea    eax,[rdx+0x6b]
  40c856:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  40c859:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  40c85c:	83 f0 25             	xor    eax,0x25
  40c85f:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  40c862:	48 b8 7d 47 5c 02 0e 	movabs rax,0x47465a0e025c477d
  40c869:	5a 46 47 
  40c86c:	48 ba 5d 0e 47 5d 0e 	movabs rdx,0x790e4f0e5d470e5d
  40c873:	4f 0e 79 
  40c876:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  40c87a:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  40c87e:	48 b8 79 4b 40 4a 57 	movabs rax,0x5d09574a404b79
  40c885:	09 5d 00 
  40c888:	48 89 45 cf          	mov    QWORD PTR [rbp-0x31],rax
  40c88c:	c7 45 b8 00 00 00 00 	mov    DWORD PTR [rbp-0x48],0x0
  40c893:	eb 1c                	jmp    40c8b1 <stderr@GLIBC_2.2.5-0x4376f>
  40c895:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40c898:	48 98                	cdqe   
  40c89a:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  40c89f:	83 f0 2e             	xor    eax,0x2e
  40c8a2:	89 c2                	mov    edx,eax
  40c8a4:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40c8a7:	48 98                	cdqe   
  40c8a9:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  40c8ad:	83 45 b8 01          	add    DWORD PTR [rbp-0x48],0x1
  40c8b1:	83 7d b8 16          	cmp    DWORD PTR [rbp-0x48],0x16
  40c8b5:	7e de                	jle    40c895 <stderr@GLIBC_2.2.5-0x4378b>
  40c8b7:	c6 45 f7 00          	mov    BYTE PTR [rbp-0x9],0x0
  40c8bb:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
  40c8bf:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  40c8c2:	0f be c0             	movsx  eax,al
  40c8c5:	83 c0 0a             	add    eax,0xa
  40c8c8:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
  40c8cb:	eb 3c                	jmp    40c909 <stderr@GLIBC_2.2.5-0x43717>
  40c8cd:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40c8d0:	83 e0 01             	and    eax,0x1
  40c8d3:	85 c0                	test   eax,eax
  40c8d5:	75 07                	jne    40c8de <stderr@GLIBC_2.2.5-0x43742>
  40c8d7:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40c8da:	d1 e8                	shr    eax,1
  40c8dc:	eb 21                	jmp    40c8ff <stderr@GLIBC_2.2.5-0x43721>
  40c8de:	8b 55 bc             	mov    edx,DWORD PTR [rbp-0x44]
  40c8e1:	89 d0                	mov    eax,edx
  40c8e3:	01 c0                	add    eax,eax
  40c8e5:	01 d0                	add    eax,edx
  40c8e7:	83 f0 fe             	xor    eax,0xfffffffe
  40c8ea:	89 c1                	mov    ecx,eax
  40c8ec:	8b 55 bc             	mov    edx,DWORD PTR [rbp-0x44]
  40c8ef:	89 d0                	mov    eax,edx
  40c8f1:	01 c0                	add    eax,eax
  40c8f3:	01 d0                	add    eax,edx
  40c8f5:	83 e0 fe             	and    eax,0xfffffffe
  40c8f8:	01 c0                	add    eax,eax
  40c8fa:	01 c8                	add    eax,ecx
  40c8fc:	83 c0 01             	add    eax,0x1
  40c8ff:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
  40c902:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  40c905:	85 c0                	test   eax,eax
  40c907:	74 08                	je     40c911 <stderr@GLIBC_2.2.5-0x4370f>
  40c909:	83 7d bc 01          	cmp    DWORD PTR [rbp-0x44],0x1
  40c90d:	75 be                	jne    40c8cd <stderr@GLIBC_2.2.5-0x43753>
  40c90f:	eb 01                	jmp    40c912 <stderr@GLIBC_2.2.5-0x4370e>
  40c911:	90                   	nop
  40c912:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  40c916:	48 89 c7             	mov    rdi,rax
  40c919:	e8 92 47 ff ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  40c91e:	bf 01 00 00 00       	mov    edi,0x1
  40c923:	e8 e8 47 ff ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  40c928:	f3 0f 1e fa          	endbr64 
  40c92c:	55                   	push   rbp
  40c92d:	48 89 e5             	mov    rbp,rsp
  40c930:	48 83 ec 60          	sub    rsp,0x60
  40c934:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  40c938:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  40c93f:	00 00 
  40c941:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  40c945:	31 c0                	xor    eax,eax
  40c947:	c7 45 b8 b9 eb 00 00 	mov    DWORD PTR [rbp-0x48],0xebb9
  40c94e:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40c951:	83 c8 18             	or     eax,0x18
  40c954:	89 c2                	mov    edx,eax
  40c956:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40c959:	83 e0 18             	and    eax,0x18
  40c95c:	01 d0                	add    eax,edx
  40c95e:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40c961:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40c964:	83 f0 80             	xor    eax,0xffffff80
  40c967:	89 c2                	mov    edx,eax
  40c969:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40c96c:	83 e0 80             	and    eax,0xffffff80
  40c96f:	01 c0                	add    eax,eax
  40c971:	01 d0                	add    eax,edx
  40c973:	83 c0 01             	add    eax,0x1
  40c976:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40c979:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40c97c:	35 5f ff ff ff       	xor    eax,0xffffff5f
  40c981:	89 c2                	mov    edx,eax
  40c983:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40c986:	24 5f                	and    al,0x5f
  40c988:	01 c0                	add    eax,eax
  40c98a:	01 d0                	add    eax,edx
  40c98c:	83 c0 01             	add    eax,0x1
  40c98f:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40c992:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40c995:	83 f0 b6             	xor    eax,0xffffffb6
  40c998:	89 c2                	mov    edx,eax
  40c99a:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40c99d:	83 e0 b6             	and    eax,0xffffffb6
  40c9a0:	01 c0                	add    eax,eax
  40c9a2:	01 d0                	add    eax,edx
  40c9a4:	83 c0 01             	add    eax,0x1
  40c9a7:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40c9aa:	48 b8 b6 81 81 9c 81 	movabs rax,0xbfd3c9819c8181b6
  40c9b1:	c9 d3 bf 
  40c9b4:	48 ba 92 8a 96 81 d3 	movabs rdx,0x83d3cbd381968a92
  40c9bb:	cb d3 83 
  40c9be:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  40c9c2:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  40c9c6:	48 b8 83 81 9c 91 9f 	movabs rax,0xdd9e969f919c8183
  40c9cd:	96 9e dd 
  40c9d0:	48 89 45 cf          	mov    QWORD PTR [rbp-0x31],rax
  40c9d4:	c7 45 bc 00 00 00 00 	mov    DWORD PTR [rbp-0x44],0x0
  40c9db:	eb 30                	jmp    40ca0d <stderr@GLIBC_2.2.5-0x43613>
  40c9dd:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40c9e0:	48 98                	cdqe   
  40c9e2:	0f b6 54 05 c0       	movzx  edx,BYTE PTR [rbp+rax*1-0x40]
  40c9e7:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40c9ea:	48 98                	cdqe   
  40c9ec:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  40c9f1:	83 e0 f3             	and    eax,0xfffffff3
  40c9f4:	8d 0c 00             	lea    ecx,[rax+rax*1]
  40c9f7:	89 d0                	mov    eax,edx
  40c9f9:	29 c8                	sub    eax,ecx
  40c9fb:	83 e8 0d             	sub    eax,0xd
  40c9fe:	89 c2                	mov    edx,eax
  40ca00:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40ca03:	48 98                	cdqe   
  40ca05:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  40ca09:	83 45 bc 01          	add    DWORD PTR [rbp-0x44],0x1
  40ca0d:	83 7d bc 16          	cmp    DWORD PTR [rbp-0x44],0x16
  40ca11:	7e ca                	jle    40c9dd <stderr@GLIBC_2.2.5-0x43643>
  40ca13:	c6 45 f7 00          	mov    BYTE PTR [rbp-0x9],0x0
  40ca17:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  40ca1b:	48 89 c7             	mov    rdi,rax
  40ca1e:	e8 8d 46 ff ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  40ca23:	bf 01 00 00 00       	mov    edi,0x1
  40ca28:	e8 e3 46 ff ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  40ca2d:	f3 0f 1e fa          	endbr64 
  40ca31:	55                   	push   rbp
  40ca32:	48 89 e5             	mov    rbp,rsp
  40ca35:	48 83 ec 70          	sub    rsp,0x70
  40ca39:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  40ca3d:	64                   	fs
  40ca3e:	48                   	rex.W
  40ca3f:	8b                   	.byte 0x8b
