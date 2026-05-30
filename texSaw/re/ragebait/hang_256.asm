
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

0000000000412167 <.text+0x11037>:
  412167:	f3 0f 1e fa          	endbr64 
  41216b:	55                   	push   rbp
  41216c:	48 89 e5             	mov    rbp,rsp
  41216f:	48 83 ec 70          	sub    rsp,0x70
  412173:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  412177:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  41217e:	00 00 
  412180:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  412184:	31 c0                	xor    eax,eax
  412186:	c7 45 a4 0e 42 00 00 	mov    DWORD PTR [rbp-0x5c],0x420e
  41218d:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  412190:	0c 88                	or     al,0x88
  412192:	89 c1                	mov    ecx,eax
  412194:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  412197:	25 88 00 00 00       	and    eax,0x88
  41219c:	89 c2                	mov    edx,eax
  41219e:	89 c8                	mov    eax,ecx
  4121a0:	29 d0                	sub    eax,edx
  4121a2:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4121a5:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4121a8:	35 2e ff ff ff       	xor    eax,0xffffff2e
  4121ad:	89 c2                	mov    edx,eax
  4121af:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4121b2:	24 2e                	and    al,0x2e
  4121b4:	01 c0                	add    eax,eax
  4121b6:	01 d0                	add    eax,edx
  4121b8:	83 c0 01             	add    eax,0x1
  4121bb:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4121be:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4121c1:	83 f0 b5             	xor    eax,0xffffffb5
  4121c4:	89 c2                	mov    edx,eax
  4121c6:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4121c9:	83 e0 b5             	and    eax,0xffffffb5
  4121cc:	01 c0                	add    eax,eax
  4121ce:	01 d0                	add    eax,edx
  4121d0:	83 c0 01             	add    eax,0x1
  4121d3:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4121d6:	48 b8 76 5b 56 12 4b 	movabs rax,0x12475d4b12565b76
  4121dd:	5d 47 12 
  4121e0:	48 ba 5f 57 53 5c 12 	movabs rdx,0x125d46125c53575f
  4121e7:	46 5d 12 
  4121ea:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  4121ee:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  4121f2:	48 b8 56 5d 12 46 5a 	movabs rax,0xd46535a46125d56
  4121f9:	53 46 0d 
  4121fc:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  412200:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  412207:	eb 31                	jmp    41223a <stderr@GLIBC_2.2.5-0x3dde6>
  412209:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  41220c:	48 98                	cdqe   
  41220e:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  412213:	83 c8 32             	or     eax,0x32
  412216:	89 c2                	mov    edx,eax
  412218:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  41221b:	48 98                	cdqe   
  41221d:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  412222:	83 e0 32             	and    eax,0x32
  412225:	89 c1                	mov    ecx,eax
  412227:	89 d0                	mov    eax,edx
  412229:	29 c8                	sub    eax,ecx
  41222b:	89 c2                	mov    edx,eax
  41222d:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  412230:	48 98                	cdqe   
  412232:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  412236:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  41223a:	83 7d a8 17          	cmp    DWORD PTR [rbp-0x58],0x17
  41223e:	7e c9                	jle    412209 <stderr@GLIBC_2.2.5-0x3de17>
  412240:	c6 45 e8 00          	mov    BYTE PTR [rbp-0x18],0x0
  412244:	c7 45 ac 00 00 00 00 	mov    DWORD PTR [rbp-0x54],0x0
  41224b:	eb 29                	jmp    412276 <stderr@GLIBC_2.2.5-0x3ddaa>
  41224d:	8b 55 a4             	mov    edx,DWORD PTR [rbp-0x5c]
  412250:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  412253:	8d 0c 02             	lea    ecx,[rdx+rax*1]
  412256:	8b 55 a4             	mov    edx,DWORD PTR [rbp-0x5c]
  412259:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  41225c:	21 d0                	and    eax,edx
  41225e:	8d 14 00             	lea    edx,[rax+rax*1]
  412261:	89 c8                	mov    eax,ecx
  412263:	29 d0                	sub    eax,edx
  412265:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  412268:	bf 64 00 00 00       	mov    edi,0x64
  41226d:	e8 ae ee fe ff       	call   401120 <stderr@GLIBC_2.2.5-0x4ef00>
  412272:	83 45 ac 01          	add    DWORD PTR [rbp-0x54],0x1
  412276:	81 7d ac 48 11 00 00 	cmp    DWORD PTR [rbp-0x54],0x1148
  41227d:	7e ce                	jle    41224d <stderr@GLIBC_2.2.5-0x3ddd3>
  41227f:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  412283:	48 89 c7             	mov    rdi,rax
  412286:	e8 25 ee fe ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  41228b:	bf 01 00 00 00       	mov    edi,0x1
  412290:	e8 7b ee fe ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  412295:	f3 0f 1e fa          	endbr64 
  412299:	55                   	push   rbp
  41229a:	48 89 e5             	mov    rbp,rsp
  41229d:	48 83 ec 60          	sub    rsp,0x60
  4122a1:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  4122a5:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  4122ac:	00 00 
  4122ae:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  4122b2:	31 c0                	xor    eax,eax
  4122b4:	c7 45 b8 26 55 00 00 	mov    DWORD PTR [rbp-0x48],0x5526
  4122bb:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  4122be:	0c ac                	or     al,0xac
  4122c0:	89 c1                	mov    ecx,eax
  4122c2:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  4122c5:	25 ac 00 00 00       	and    eax,0xac
  4122ca:	89 c2                	mov    edx,eax
  4122cc:	89 c8                	mov    eax,ecx
  4122ce:	29 d0                	sub    eax,edx
  4122d0:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  4122d3:	8b 55 b8             	mov    edx,DWORD PTR [rbp-0x48]
  4122d6:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  4122d9:	83 e0 32             	and    eax,0x32
  4122dc:	01 c0                	add    eax,eax
  4122de:	29 c2                	sub    edx,eax
  4122e0:	8d 42 32             	lea    eax,[rdx+0x32]
  4122e3:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  4122e6:	48 b8 48 4b 59 42 10 	movabs rax,0x45490a1042594b48
  4122ed:	0a 49 45 
  4122f0:	48 ba 47 47 4b 44 4e 	movabs rdx,0x45440a4e444b4747
  4122f7:	0a 44 45 
  4122fa:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  4122fe:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  412302:	48 b8 45 5e 0a 4c 45 	movabs rax,0x4e445f454c0a5e45
  412309:	5f 44 4e 
  41230c:	48 89 45 cf          	mov    QWORD PTR [rbp-0x31],rax
  412310:	c7 45 bc 00 00 00 00 	mov    DWORD PTR [rbp-0x44],0x0
  412317:	eb 30                	jmp    412349 <stderr@GLIBC_2.2.5-0x3dcd7>
  412319:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  41231c:	48 98                	cdqe   
  41231e:	0f b6 54 05 c0       	movzx  edx,BYTE PTR [rbp+rax*1-0x40]
  412323:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  412326:	48 98                	cdqe   
  412328:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  41232d:	83 e0 2a             	and    eax,0x2a
  412330:	8d 0c 00             	lea    ecx,[rax+rax*1]
  412333:	89 d0                	mov    eax,edx
  412335:	29 c8                	sub    eax,ecx
  412337:	83 c0 2a             	add    eax,0x2a
  41233a:	89 c2                	mov    edx,eax
  41233c:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  41233f:	48 98                	cdqe   
  412341:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  412345:	83 45 bc 01          	add    DWORD PTR [rbp-0x44],0x1
  412349:	83 7d bc 16          	cmp    DWORD PTR [rbp-0x44],0x16
  41234d:	7e ca                	jle    412319 <stderr@GLIBC_2.2.5-0x3dd07>
  41234f:	c6 45 f7 00          	mov    BYTE PTR [rbp-0x9],0x0
  412353:	48 8b 55 a8          	mov    rdx,QWORD PTR [rbp-0x58]
  412357:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  41235b:	48 89 c6             	mov    rsi,rax
  41235e:	48 8d 05 e2 1c 03 00 	lea    rax,[rip+0x31ce2]        # 444047 <stderr@GLIBC_2.2.5-0xbfd9>
  412365:	48 89 c7             	mov    rdi,rax
  412368:	b8 00 00 00 00       	mov    eax,0x0
  41236d:	e8 6e ed fe ff       	call   4010e0 <stderr@GLIBC_2.2.5-0x4ef40>
  412372:	bf 7f 00 00 00       	mov    edi,0x7f
  412377:	e8 94 ed fe ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  41237c:	f3 0f 1e fa          	endbr64 
  412380:	55                   	push   rbp
  412381:	48 89 e5             	mov    rbp,rsp
  412384:	48                   	rex.W
  412385:	83                   	.byte 0x83
  412386:	ec                   	in     al,dx
