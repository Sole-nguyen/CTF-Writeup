
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

000000000040da15 <.text+0xc8e5>:
  40da15:	f3 0f 1e fa          	endbr64 
  40da19:	55                   	push   rbp
  40da1a:	48 89 e5             	mov    rbp,rsp
  40da1d:	48 83 ec 70          	sub    rsp,0x70
  40da21:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  40da25:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  40da2c:	00 00 
  40da2e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  40da32:	31 c0                	xor    eax,eax
  40da34:	c7 45 a4 67 7c 00 00 	mov    DWORD PTR [rbp-0x5c],0x7c67
  40da3b:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40da3e:	0c b7                	or     al,0xb7
  40da40:	89 c1                	mov    ecx,eax
  40da42:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40da45:	25 b7 00 00 00       	and    eax,0xb7
  40da4a:	89 c2                	mov    edx,eax
  40da4c:	89 c8                	mov    eax,ecx
  40da4e:	29 d0                	sub    eax,edx
  40da50:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  40da53:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40da56:	35 70 ff ff ff       	xor    eax,0xffffff70
  40da5b:	89 c2                	mov    edx,eax
  40da5d:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40da60:	24 70                	and    al,0x70
  40da62:	01 c0                	add    eax,eax
  40da64:	01 d0                	add    eax,edx
  40da66:	83 c0 01             	add    eax,0x1
  40da69:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  40da6c:	48 b8 d8 f5 f8 bc e5 	movabs rax,0xbce9f3e5bcf8f5d8
  40da73:	f3 e9 bc 
  40da76:	48 ba f1 f9 fd f2 bc 	movabs rdx,0xbcf3e8bcf2fdf9f1
  40da7d:	e8 f3 bc 
  40da80:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  40da84:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  40da88:	48 b8 f8 f3 bc e8 f4 	movabs rax,0xa3e8fdf4e8bcf3f8
  40da8f:	fd e8 a3 
  40da92:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  40da96:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  40da9d:	eb 31                	jmp    40dad0 <stderr@GLIBC_2.2.5-0x42550>
  40da9f:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  40daa2:	48 98                	cdqe   
  40daa4:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  40daa9:	83 c8 9c             	or     eax,0xffffff9c
  40daac:	89 c2                	mov    edx,eax
  40daae:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  40dab1:	48 98                	cdqe   
  40dab3:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  40dab8:	83 e0 9c             	and    eax,0xffffff9c
  40dabb:	89 c1                	mov    ecx,eax
  40dabd:	89 d0                	mov    eax,edx
  40dabf:	29 c8                	sub    eax,ecx
  40dac1:	89 c2                	mov    edx,eax
  40dac3:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  40dac6:	48 98                	cdqe   
  40dac8:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  40dacc:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  40dad0:	83 7d a8 17          	cmp    DWORD PTR [rbp-0x58],0x17
  40dad4:	7e c9                	jle    40da9f <stderr@GLIBC_2.2.5-0x42581>
  40dad6:	c6 45 e8 00          	mov    BYTE PTR [rbp-0x18],0x0
  40dada:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
  40dade:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  40dae1:	0f be c0             	movsx  eax,al
  40dae4:	83 c0 03             	add    eax,0x3
  40dae7:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  40daea:	eb 3c                	jmp    40db28 <stderr@GLIBC_2.2.5-0x424f8>
  40daec:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  40daef:	83 e0 01             	and    eax,0x1
  40daf2:	85 c0                	test   eax,eax
  40daf4:	75 07                	jne    40dafd <stderr@GLIBC_2.2.5-0x42523>
  40daf6:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  40daf9:	d1 e8                	shr    eax,1
  40dafb:	eb 21                	jmp    40db1e <stderr@GLIBC_2.2.5-0x42502>
  40dafd:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  40db00:	89 d0                	mov    eax,edx
  40db02:	01 c0                	add    eax,eax
  40db04:	01 d0                	add    eax,edx
  40db06:	83 f0 fe             	xor    eax,0xfffffffe
  40db09:	89 c1                	mov    ecx,eax
  40db0b:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  40db0e:	89 d0                	mov    eax,edx
  40db10:	01 c0                	add    eax,eax
  40db12:	01 d0                	add    eax,edx
  40db14:	83 e0 fe             	and    eax,0xfffffffe
  40db17:	01 c0                	add    eax,eax
  40db19:	01 c8                	add    eax,ecx
  40db1b:	83 c0 01             	add    eax,0x1
  40db1e:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  40db21:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40db24:	85 c0                	test   eax,eax
  40db26:	74 08                	je     40db30 <stderr@GLIBC_2.2.5-0x424f0>
  40db28:	83 7d ac 01          	cmp    DWORD PTR [rbp-0x54],0x1
  40db2c:	75 be                	jne    40daec <stderr@GLIBC_2.2.5-0x42534>
  40db2e:	eb 01                	jmp    40db31 <stderr@GLIBC_2.2.5-0x424ef>
  40db30:	90                   	nop
  40db31:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  40db35:	48 89 c7             	mov    rdi,rax
  40db38:	e8 73 35 ff ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  40db3d:	bf 01 00 00 00       	mov    edi,0x1
  40db42:	e8 c9 35 ff ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  40db47:	f3 0f 1e fa          	endbr64 
  40db4b:	55                   	push   rbp
  40db4c:	48 89 e5             	mov    rbp,rsp
  40db4f:	48 83 ec 60          	sub    rsp,0x60
  40db53:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  40db57:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  40db5e:	00 00 
  40db60:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  40db64:	31 c0                	xor    eax,eax
  40db66:	c7 45 b8 60 a0 00 00 	mov    DWORD PTR [rbp-0x48],0xa060
  40db6d:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40db70:	34 83                	xor    al,0x83
  40db72:	89 c2                	mov    edx,eax
  40db74:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40db77:	25 83 00 00 00       	and    eax,0x83
  40db7c:	01 c0                	add    eax,eax
  40db7e:	01 d0                	add    eax,edx
  40db80:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40db83:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40db86:	83 c8 79             	or     eax,0x79
  40db89:	89 c1                	mov    ecx,eax
  40db8b:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40db8e:	83 e0 79             	and    eax,0x79
  40db91:	89 c2                	mov    edx,eax
  40db93:	89 c8                	mov    eax,ecx
  40db95:	29 d0                	sub    eax,edx
  40db97:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40db9a:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40db9d:	83 f0 de             	xor    eax,0xffffffde
  40dba0:	89 c2                	mov    edx,eax
  40dba2:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40dba5:	83 e0 de             	and    eax,0xffffffde
  40dba8:	01 c0                	add    eax,eax
  40dbaa:	01 d0                	add    eax,edx
  40dbac:	83 c0 01             	add    eax,0x1
  40dbaf:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40dbb2:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40dbb5:	35 12 ff ff ff       	xor    eax,0xffffff12
  40dbba:	89 c2                	mov    edx,eax
  40dbbc:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40dbbf:	24 12                	and    al,0x12
  40dbc1:	01 c0                	add    eax,eax
  40dbc3:	01 d0                	add    eax,edx
  40dbc5:	83 c0 01             	add    eax,0x1
  40dbc8:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40dbcb:	48 b8 a2 a1 b3 a8 fa 	movabs rax,0xafa3e0faa8b3a1a2
  40dbd2:	e0 a3 af 
  40dbd5:	48 ba ad ad a1 ae a4 	movabs rdx,0xafaee0a4aea1adad
  40dbdc:	e0 ae af 
  40dbdf:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  40dbe3:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  40dbe7:	48 b8 af b4 e0 a6 af 	movabs rax,0xa4aeb5afa6e0b4af
  40dbee:	b5 ae a4 
  40dbf1:	48 89 45 cf          	mov    QWORD PTR [rbp-0x31],rax
  40dbf5:	c7 45 bc 00 00 00 00 	mov    DWORD PTR [rbp-0x44],0x0
  40dbfc:	eb 30                	jmp    40dc2e <stderr@GLIBC_2.2.5-0x423f2>
  40dbfe:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40dc01:	48 98                	cdqe   
  40dc03:	0f b6 54 05 c0       	movzx  edx,BYTE PTR [rbp+rax*1-0x40]
  40dc08:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40dc0b:	48 98                	cdqe   
  40dc0d:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  40dc12:	83 e0 c0             	and    eax,0xffffffc0
  40dc15:	8d 0c 00             	lea    ecx,[rax+rax*1]
  40dc18:	89 d0                	mov    eax,edx
  40dc1a:	29 c8                	sub    eax,ecx
  40dc1c:	83 e8 40             	sub    eax,0x40
  40dc1f:	89 c2                	mov    edx,eax
  40dc21:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  40dc24:	48 98                	cdqe   
  40dc26:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  40dc2a:	83 45 bc 01          	add    DWORD PTR [rbp-0x44],0x1
  40dc2e:	83 7d bc 16          	cmp    DWORD PTR [rbp-0x44],0x16
  40dc32:	7e ca                	jle    40dbfe <stderr@GLIBC_2.2.5-0x42422>
  40dc34:	c6                   	.byte 0xc6
