
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

0000000000411d85 <.text+0x10c55>:
  411d85:	f3 0f 1e fa          	endbr64 
  411d89:	55                   	push   rbp
  411d8a:	48 89 e5             	mov    rbp,rsp
  411d8d:	48 83 ec 60          	sub    rsp,0x60
  411d91:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  411d95:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  411d9c:	00 00 
  411d9e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  411da2:	31 c0                	xor    eax,eax
  411da4:	c7 45 b4 47 3a 00 00 	mov    DWORD PTR [rbp-0x4c],0x3a47
  411dab:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  411dae:	83 f0 43             	xor    eax,0x43
  411db1:	89 c2                	mov    edx,eax
  411db3:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  411db6:	83 e0 43             	and    eax,0x43
  411db9:	01 c0                	add    eax,eax
  411dbb:	01 d0                	add    eax,edx
  411dbd:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  411dc0:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  411dc3:	83 c8 66             	or     eax,0x66
  411dc6:	89 c2                	mov    edx,eax
  411dc8:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  411dcb:	83 e0 66             	and    eax,0x66
  411dce:	01 d0                	add    eax,edx
  411dd0:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  411dd3:	48 b8 c6 f1 f1 ec f1 	movabs rax,0xcfa3b9f1ecf1f1c6
  411dda:	b9 a3 cf 
  411ddd:	48 ba e2 fa e6 f1 a3 	movabs rdx,0xf3a3bba3f1e6fae2
  411de4:	bb a3 f3 
  411de7:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  411deb:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  411def:	48 b8 f3 f1 ec e1 ef 	movabs rax,0xadeee6efe1ecf1f3
  411df6:	e6 ee ad 
  411df9:	48 89 45 cf          	mov    QWORD PTR [rbp-0x31],rax
  411dfd:	c7 45 b8 00 00 00 00 	mov    DWORD PTR [rbp-0x48],0x0
  411e04:	eb 30                	jmp    411e36 <stderr@GLIBC_2.2.5-0x3e1ea>
  411e06:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  411e09:	48 98                	cdqe   
  411e0b:	0f b6 54 05 c0       	movzx  edx,BYTE PTR [rbp+rax*1-0x40]
  411e10:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  411e13:	48 98                	cdqe   
  411e15:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  411e1a:	83 e0 83             	and    eax,0xffffff83
  411e1d:	8d 0c 00             	lea    ecx,[rax+rax*1]
  411e20:	89 d0                	mov    eax,edx
  411e22:	29 c8                	sub    eax,ecx
  411e24:	83 e8 7d             	sub    eax,0x7d
  411e27:	89 c2                	mov    edx,eax
  411e29:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  411e2c:	48 98                	cdqe   
  411e2e:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  411e32:	83 45 b8 01          	add    DWORD PTR [rbp-0x48],0x1
  411e36:	83 7d b8 16          	cmp    DWORD PTR [rbp-0x48],0x16
  411e3a:	7e ca                	jle    411e06 <stderr@GLIBC_2.2.5-0x3e21a>
  411e3c:	c6 45 f7 00          	mov    BYTE PTR [rbp-0x9],0x0
  411e40:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
  411e44:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  411e47:	0f be c0             	movsx  eax,al
  411e4a:	83 c0 06             	add    eax,0x6
  411e4d:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
  411e50:	eb 3c                	jmp    411e8e <stderr@GLIBC_2.2.5-0x3e192>
  411e52:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  411e55:	83 e0 01             	and    eax,0x1
  411e58:	85 c0                	test   eax,eax
  411e5a:	75 07                	jne    411e63 <stderr@GLIBC_2.2.5-0x3e1bd>
  411e5c:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  411e5f:	d1 e8                	shr    eax,1
  411e61:	eb 21                	jmp    411e84 <stderr@GLIBC_2.2.5-0x3e19c>
  411e63:	8b 55 bc             	mov    edx,DWORD PTR [rbp-0x44]
  411e66:	89 d0                	mov    eax,edx
  411e68:	01 c0                	add    eax,eax
  411e6a:	01 d0                	add    eax,edx
  411e6c:	83 f0 fe             	xor    eax,0xfffffffe
  411e6f:	89 c1                	mov    ecx,eax
  411e71:	8b 55 bc             	mov    edx,DWORD PTR [rbp-0x44]
  411e74:	89 d0                	mov    eax,edx
  411e76:	01 c0                	add    eax,eax
  411e78:	01 d0                	add    eax,edx
  411e7a:	83 e0 fe             	and    eax,0xfffffffe
  411e7d:	01 c0                	add    eax,eax
  411e7f:	01 c8                	add    eax,ecx
  411e81:	83 c0 01             	add    eax,0x1
  411e84:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
  411e87:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  411e8a:	85 c0                	test   eax,eax
  411e8c:	74 08                	je     411e96 <stderr@GLIBC_2.2.5-0x3e18a>
  411e8e:	83 7d bc 01          	cmp    DWORD PTR [rbp-0x44],0x1
  411e92:	75 be                	jne    411e52 <stderr@GLIBC_2.2.5-0x3e1ce>
  411e94:	eb 01                	jmp    411e97 <stderr@GLIBC_2.2.5-0x3e189>
  411e96:	90                   	nop
  411e97:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  411e9b:	48 89 c7             	mov    rdi,rax
  411e9e:	e8 0d f2 fe ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  411ea3:	bf 01 00 00 00       	mov    edi,0x1
  411ea8:	e8 63 f2 fe ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  411ead:	f3 0f 1e fa          	endbr64 
  411eb1:	55                   	push   rbp
  411eb2:	48 89 e5             	mov    rbp,rsp
  411eb5:	48 83 ec 70          	sub    rsp,0x70
  411eb9:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  411ebd:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  411ec4:	00 00 
  411ec6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  411eca:	31 c0                	xor    eax,eax
  411ecc:	c7 45 a8 8e b6 00 00 	mov    DWORD PTR [rbp-0x58],0xb68e
  411ed3:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  411ed6:	35 26 ff ff ff       	xor    eax,0xffffff26
  411edb:	89 c2                	mov    edx,eax
  411edd:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  411ee0:	24 26                	and    al,0x26
  411ee2:	01 c0                	add    eax,eax
  411ee4:	01 d0                	add    eax,edx
  411ee6:	83 c0 01             	add    eax,0x1
  411ee9:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
  411eec:	8b 55 a8             	mov    edx,DWORD PTR [rbp-0x58]
  411eef:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  411ef2:	25 c7 00 00 00       	and    eax,0xc7
  411ef7:	01 c0                	add    eax,eax
  411ef9:	29 c2                	sub    edx,eax
  411efb:	8d 82 c7 00 00 00    	lea    eax,[rdx+0xc7]
  411f01:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
  411f04:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  411f07:	83 c8 74             	or     eax,0x74
  411f0a:	89 c2                	mov    edx,eax
  411f0c:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  411f0f:	83 e0 74             	and    eax,0x74
  411f12:	01 d0                	add    eax,edx
  411f14:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
  411f17:	48 b8 fa cd cd d0 cd 	movabs rax,0x8e8b9fcdd0cdcdfa
  411f1e:	9f 8b 8e 
  411f21:	48 ba 87 85 9f f6 98 	movabs rdx,0xde9fd298f69f8587
  411f28:	d2 9f de 
  411f2b:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  411f2f:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  411f33:	48 b8 9f cb da de cf 	movabs rax,0x91cbd0cfdedacb9f
  411f3a:	d0 cb 91 
  411f3d:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  411f41:	c7 45 ac 00 00 00 00 	mov    DWORD PTR [rbp-0x54],0x0
  411f48:	eb 31                	jmp    411f7b <stderr@GLIBC_2.2.5-0x3e0a5>
  411f4a:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  411f4d:	48 98                	cdqe   
  411f4f:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  411f54:	83 c8 bf             	or     eax,0xffffffbf
  411f57:	89 c2                	mov    edx,eax
  411f59:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  411f5c:	48 98                	cdqe   
  411f5e:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  411f63:	83 e0 bf             	and    eax,0xffffffbf
  411f66:	89 c1                	mov    ecx,eax
  411f68:	89 d0                	mov    eax,edx
  411f6a:	29 c8                	sub    eax,ecx
  411f6c:	89 c2                	mov    edx,eax
  411f6e:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  411f71:	48 98                	cdqe   
  411f73:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  411f77:	83 45 ac 01          	add    DWORD PTR [rbp-0x54],0x1
  411f7b:	83 7d ac 17          	cmp    DWORD PTR [rbp-0x54],0x17
  411f7f:	7e c9                	jle    411f4a <stderr@GLIBC_2.2.5-0x3e0d6>
  411f81:	c6 45 e8 00          	mov    BYTE PTR [rbp-0x18],0x0
  411f85:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  411f89:	48 89 c7             	mov    rdi,rax
  411f8c:	e8 1f f1 fe ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  411f91:	bf 01 00 00 00       	mov    edi,0x1
  411f96:	e8 75 f1 fe ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  411f9b:	f3 0f 1e fa          	endbr64 
  411f9f:	55                   	push   rbp
  411fa0:	48 89 e5             	mov    rbp,rsp
  411fa3:	48                   	rex.W
  411fa4:	83                   	.byte 0x83
