
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

0000000000410191 <.text+0xf061>:
  410191:	f3 0f 1e fa          	endbr64 
  410195:	55                   	push   rbp
  410196:	48 89 e5             	mov    rbp,rsp
  410199:	48 83 ec 70          	sub    rsp,0x70
  41019d:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  4101a1:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  4101a8:	00 00 
  4101aa:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  4101ae:	31 c0                	xor    eax,eax
  4101b0:	c7 45 a4 8f 9e 00 00 	mov    DWORD PTR [rbp-0x5c],0x9e8f
  4101b7:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4101ba:	83 f0 2e             	xor    eax,0x2e
  4101bd:	89 c2                	mov    edx,eax
  4101bf:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4101c2:	83 e0 2e             	and    eax,0x2e
  4101c5:	01 c0                	add    eax,eax
  4101c7:	01 d0                	add    eax,edx
  4101c9:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4101cc:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4101cf:	35 28 ff ff ff       	xor    eax,0xffffff28
  4101d4:	89 c2                	mov    edx,eax
  4101d6:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4101d9:	24 28                	and    al,0x28
  4101db:	01 c0                	add    eax,eax
  4101dd:	01 d0                	add    eax,edx
  4101df:	83 c0 01             	add    eax,0x1
  4101e2:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4101e5:	48 b8 7f 42 11 45 16 	movabs rax,0x425958164511427f
  4101ec:	58 59 42 
  4101ef:	48 ba 16 57 16 54 43 	movabs rdx,0x161a514354165716
  4101f6:	51 1a 16 
  4101f9:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  4101fd:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  410201:	48 b8 16 5f 42 11 45 	movabs rax,0x1657164511425f16
  410208:	16 57 16 
  41020b:	48 ba 50 53 57 42 43 	movabs rdx,0x1753444342575350
  410212:	44 53 17 
  410215:	48 89 45 bf          	mov    QWORD PTR [rbp-0x41],rax
  410219:	48 89 55 c7          	mov    QWORD PTR [rbp-0x39],rdx
  41021d:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  410224:	eb 31                	jmp    410257 <stderr@GLIBC_2.2.5-0x3fdc9>
  410226:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  410229:	48 98                	cdqe   
  41022b:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  410230:	83 c8 36             	or     eax,0x36
  410233:	89 c2                	mov    edx,eax
  410235:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  410238:	48 98                	cdqe   
  41023a:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  41023f:	83 e0 36             	and    eax,0x36
  410242:	89 c1                	mov    ecx,eax
  410244:	89 d0                	mov    eax,edx
  410246:	29 c8                	sub    eax,ecx
  410248:	89 c2                	mov    edx,eax
  41024a:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  41024d:	48 98                	cdqe   
  41024f:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  410253:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  410257:	83 7d a8 1e          	cmp    DWORD PTR [rbp-0x58],0x1e
  41025b:	7e c9                	jle    410226 <stderr@GLIBC_2.2.5-0x3fdfa>
  41025d:	c6 45 ef 00          	mov    BYTE PTR [rbp-0x11],0x0
  410261:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
  410265:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  410268:	0f be c0             	movsx  eax,al
  41026b:	83 c0 06             	add    eax,0x6
  41026e:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  410271:	eb 3c                	jmp    4102af <stderr@GLIBC_2.2.5-0x3fd71>
  410273:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  410276:	83 e0 01             	and    eax,0x1
  410279:	85 c0                	test   eax,eax
  41027b:	75 07                	jne    410284 <stderr@GLIBC_2.2.5-0x3fd9c>
  41027d:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  410280:	d1 e8                	shr    eax,1
  410282:	eb 21                	jmp    4102a5 <stderr@GLIBC_2.2.5-0x3fd7b>
  410284:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  410287:	89 d0                	mov    eax,edx
  410289:	01 c0                	add    eax,eax
  41028b:	01 d0                	add    eax,edx
  41028d:	83 f0 fe             	xor    eax,0xfffffffe
  410290:	89 c1                	mov    ecx,eax
  410292:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  410295:	89 d0                	mov    eax,edx
  410297:	01 c0                	add    eax,eax
  410299:	01 d0                	add    eax,edx
  41029b:	83 e0 fe             	and    eax,0xfffffffe
  41029e:	01 c0                	add    eax,eax
  4102a0:	01 c8                	add    eax,ecx
  4102a2:	83 c0 01             	add    eax,0x1
  4102a5:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  4102a8:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4102ab:	85 c0                	test   eax,eax
  4102ad:	74 08                	je     4102b7 <stderr@GLIBC_2.2.5-0x3fd69>
  4102af:	83 7d ac 01          	cmp    DWORD PTR [rbp-0x54],0x1
  4102b3:	75 be                	jne    410273 <stderr@GLIBC_2.2.5-0x3fdad>
  4102b5:	eb 01                	jmp    4102b8 <stderr@GLIBC_2.2.5-0x3fd68>
  4102b7:	90                   	nop
  4102b8:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  4102bc:	48 89 c7             	mov    rdi,rax
  4102bf:	e8 ec 0d ff ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  4102c4:	bf 01 00 00 00       	mov    edi,0x1
  4102c9:	e8 42 0e ff ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  4102ce:	f3 0f 1e fa          	endbr64 
  4102d2:	55                   	push   rbp
  4102d3:	48 89 e5             	mov    rbp,rsp
  4102d6:	48 83 ec 60          	sub    rsp,0x60
  4102da:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  4102de:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  4102e5:	00 00 
  4102e7:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  4102eb:	31 c0                	xor    eax,eax
  4102ed:	c7 45 b4 54 a4 00 00 	mov    DWORD PTR [rbp-0x4c],0xa454
  4102f4:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  4102f7:	34 98                	xor    al,0x98
  4102f9:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  4102fc:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  4102ff:	0c f7                	or     al,0xf7
  410301:	89 c2                	mov    edx,eax
  410303:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  410306:	25 f7 00 00 00       	and    eax,0xf7
  41030b:	01 d0                	add    eax,edx
  41030d:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  410310:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  410313:	83 f0 8a             	xor    eax,0xffffff8a
  410316:	89 c2                	mov    edx,eax
  410318:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  41031b:	83 e0 8a             	and    eax,0xffffff8a
  41031e:	01 c0                	add    eax,eax
  410320:	01 d0                	add    eax,edx
  410322:	83 c0 01             	add    eax,0x1
  410325:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  410328:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  41032b:	35 77 ff ff ff       	xor    eax,0xffffff77
  410330:	89 c2                	mov    edx,eax
  410332:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  410335:	24 77                	and    al,0x77
  410337:	01 c0                	add    eax,eax
  410339:	01 d0                	add    eax,edx
  41033b:	83 c0 01             	add    eax,0x1
  41033e:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  410341:	48 b8 f1 c6 c6 db c6 	movabs rax,0xf8948ec6dbc6c6f1
  410348:	8e 94 f8 
  41034b:	48 ba d5 cd d1 c6 94 	movabs rdx,0xc4948c94c6d1cdd5
  410352:	8c 94 c4 
  410355:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  410359:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  41035d:	48 b8 c4 c6 db d6 d8 	movabs rax,0x9ad9d1d8d6dbc6c4
  410364:	d1 d9 9a 
  410367:	48 89 45 cf          	mov    QWORD PTR [rbp-0x31],rax
  41036b:	c7 45 b8 00 00 00 00 	mov    DWORD PTR [rbp-0x48],0x0
  410372:	eb 30                	jmp    4103a4 <stderr@GLIBC_2.2.5-0x3fc7c>
  410374:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  410377:	48 98                	cdqe   
  410379:	0f b6 54 05 c0       	movzx  edx,BYTE PTR [rbp+rax*1-0x40]
  41037e:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  410381:	48 98                	cdqe   
  410383:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  410388:	83 e0 b4             	and    eax,0xffffffb4
  41038b:	8d 0c 00             	lea    ecx,[rax+rax*1]
  41038e:	89 d0                	mov    eax,edx
  410390:	29 c8                	sub    eax,ecx
  410392:	83 e8 4c             	sub    eax,0x4c
  410395:	89 c2                	mov    edx,eax
  410397:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  41039a:	48 98                	cdqe   
  41039c:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  4103a0:	83 45 b8 01          	add    DWORD PTR [rbp-0x48],0x1
  4103a4:	83 7d b8 16          	cmp    DWORD PTR [rbp-0x48],0x16
  4103a8:	7e ca                	jle    410374 <stderr@GLIBC_2.2.5-0x3fcac>
  4103aa:	c6 45 f7 00          	mov    BYTE PTR [rbp-0x9],0x0
  4103ae:	c7                   	.byte 0xc7
  4103af:	45                   	rex.RB
  4103b0:	bc                   	.byte 0xbc
