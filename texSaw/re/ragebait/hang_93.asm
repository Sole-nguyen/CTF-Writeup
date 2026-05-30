
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

00000000004073fc <.text+0x62cc>:
  4073fc:	f3 0f 1e fa          	endbr64 
  407400:	55                   	push   rbp
  407401:	48 89 e5             	mov    rbp,rsp
  407404:	48 83 ec 70          	sub    rsp,0x70
  407408:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  40740c:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  407413:	00 00 
  407415:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  407419:	31 c0                	xor    eax,eax
  40741b:	c7 45 a4 f4 1a 00 00 	mov    DWORD PTR [rbp-0x5c],0x1af4
  407422:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  407425:	35 32 ff ff ff       	xor    eax,0xffffff32
  40742a:	89 c2                	mov    edx,eax
  40742c:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40742f:	24 32                	and    al,0x32
  407431:	01 c0                	add    eax,eax
  407433:	01 d0                	add    eax,edx
  407435:	83 c0 01             	add    eax,0x1
  407438:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  40743b:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  40743e:	83 c8 47             	or     eax,0x47
  407441:	89 c2                	mov    edx,eax
  407443:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  407446:	83 e0 47             	and    eax,0x47
  407449:	01 d0                	add    eax,edx
  40744b:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  40744e:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  407451:	83 f0 dd             	xor    eax,0xffffffdd
  407454:	89 c2                	mov    edx,eax
  407456:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  407459:	83 e0 dd             	and    eax,0xffffffdd
  40745c:	01 c0                	add    eax,eax
  40745e:	01 d0                	add    eax,edx
  407460:	83 c0 01             	add    eax,0x1
  407463:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  407466:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  407469:	35 53 ff ff ff       	xor    eax,0xffffff53
  40746e:	89 c2                	mov    edx,eax
  407470:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  407473:	24 53                	and    al,0x53
  407475:	01 c0                	add    eax,eax
  407477:	01 d0                	add    eax,edx
  407479:	83 c0 01             	add    eax,0x1
  40747c:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  40747f:	48 b8 5a 6f 7d 65 2e 	movabs rax,0x676f682e657d6f5a
  407486:	68 6f 67 
  407489:	48 ba 62 6b 6a 2e 7d 	movabs rdx,0x6d6d7b7d2e6a6b62
  407490:	7b 6d 6d 
  407493:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  407497:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  40749b:	48 b8 6b 6a 2e 7d 7b 	movabs rax,0x6b6d6d7b7d2e6a6b
  4074a2:	6d 6d 6b 
  4074a5:	48 ba 7d 7d 68 7b 62 	movabs rdx,0x207762627b687d7d
  4074ac:	62 77 20 
  4074af:	48 89 45 b9          	mov    QWORD PTR [rbp-0x47],rax
  4074b3:	48 89 55 c1          	mov    QWORD PTR [rbp-0x3f],rdx
  4074b7:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  4074be:	eb 1c                	jmp    4074dc <stderr@GLIBC_2.2.5-0x48b44>
  4074c0:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  4074c3:	48 98                	cdqe   
  4074c5:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  4074ca:	83 f0 0e             	xor    eax,0xe
  4074cd:	89 c2                	mov    edx,eax
  4074cf:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  4074d2:	48 98                	cdqe   
  4074d4:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  4074d8:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  4074dc:	83 7d a8 18          	cmp    DWORD PTR [rbp-0x58],0x18
  4074e0:	7e de                	jle    4074c0 <stderr@GLIBC_2.2.5-0x48b60>
  4074e2:	c6 45 e9 00          	mov    BYTE PTR [rbp-0x17],0x0
  4074e6:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
  4074ea:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  4074ed:	0f be c0             	movsx  eax,al
  4074f0:	83 c0 07             	add    eax,0x7
  4074f3:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  4074f6:	eb 3c                	jmp    407534 <stderr@GLIBC_2.2.5-0x48aec>
  4074f8:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  4074fb:	83 e0 01             	and    eax,0x1
  4074fe:	85 c0                	test   eax,eax
  407500:	75 07                	jne    407509 <stderr@GLIBC_2.2.5-0x48b17>
  407502:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  407505:	d1 e8                	shr    eax,1
  407507:	eb 21                	jmp    40752a <stderr@GLIBC_2.2.5-0x48af6>
  407509:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  40750c:	89 d0                	mov    eax,edx
  40750e:	01 c0                	add    eax,eax
  407510:	01 d0                	add    eax,edx
  407512:	83 f0 fe             	xor    eax,0xfffffffe
  407515:	89 c1                	mov    ecx,eax
  407517:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  40751a:	89 d0                	mov    eax,edx
  40751c:	01 c0                	add    eax,eax
  40751e:	01 d0                	add    eax,edx
  407520:	83 e0 fe             	and    eax,0xfffffffe
  407523:	01 c0                	add    eax,eax
  407525:	01 c8                	add    eax,ecx
  407527:	83 c0 01             	add    eax,0x1
  40752a:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  40752d:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  407530:	85 c0                	test   eax,eax
  407532:	74 08                	je     40753c <stderr@GLIBC_2.2.5-0x48ae4>
  407534:	83 7d ac 01          	cmp    DWORD PTR [rbp-0x54],0x1
  407538:	75 be                	jne    4074f8 <stderr@GLIBC_2.2.5-0x48b28>
  40753a:	eb 01                	jmp    40753d <stderr@GLIBC_2.2.5-0x48ae3>
  40753c:	90                   	nop
  40753d:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  407541:	48 89 c7             	mov    rdi,rax
  407544:	e8 67 9b ff ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  407549:	bf 01 00 00 00       	mov    edi,0x1
  40754e:	e8 bd 9b ff ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  407553:	f3 0f 1e fa          	endbr64 
  407557:	55                   	push   rbp
  407558:	48 89 e5             	mov    rbp,rsp
  40755b:	48 83 ec 70          	sub    rsp,0x70
  40755f:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  407563:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  40756a:	00 00 
  40756c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  407570:	31 c0                	xor    eax,eax
  407572:	c7 45 a8 ce 32 00 00 	mov    DWORD PTR [rbp-0x58],0x32ce
  407579:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  40757c:	83 f0 0d             	xor    eax,0xd
  40757f:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
  407582:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  407585:	83 f0 f6             	xor    eax,0xfffffff6
  407588:	89 c2                	mov    edx,eax
  40758a:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  40758d:	83 e0 f6             	and    eax,0xfffffff6
  407590:	01 c0                	add    eax,eax
  407592:	01 d0                	add    eax,edx
  407594:	83 c0 01             	add    eax,0x1
  407597:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
  40759a:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  40759d:	83 f0 03             	xor    eax,0x3
  4075a0:	89 c2                	mov    edx,eax
  4075a2:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  4075a5:	83 e0 03             	and    eax,0x3
  4075a8:	01 c0                	add    eax,eax
  4075aa:	01 d0                	add    eax,edx
  4075ac:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
  4075af:	48 b8 7e 4b 59 41 0a 	movabs rax,0x434b4c0a41594b7e
  4075b6:	4c 4b 43 
  4075b9:	48 ba 46 4f 4e 0a 59 	movabs rdx,0x49495f590a4e4f46
  4075c0:	5f 49 49 
  4075c3:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  4075c7:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  4075cb:	48 b8 4f 4e 0a 59 5f 	movabs rax,0x4f49495f590a4e4f
  4075d2:	49 49 4f 
  4075d5:	48 ba 59 59 4c 5f 46 	movabs rdx,0x45346465f4c5959
  4075dc:	46 53 04 
  4075df:	48 89 45 b9          	mov    QWORD PTR [rbp-0x47],rax
  4075e3:	48 89 55 c1          	mov    QWORD PTR [rbp-0x3f],rdx
  4075e7:	c7 45 ac 00 00 00 00 	mov    DWORD PTR [rbp-0x54],0x0
  4075ee:	eb 30                	jmp    407620 <stderr@GLIBC_2.2.5-0x48a00>
  4075f0:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  4075f3:	48 98                	cdqe   
  4075f5:	0f b6 54 05 b0       	movzx  edx,BYTE PTR [rbp+rax*1-0x50]
  4075fa:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  4075fd:	48 98                	cdqe   
  4075ff:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  407604:	83 e0 2a             	and    eax,0x2a
  407607:	8d 0c 00             	lea    ecx,[rax+rax*1]
  40760a:	89 d0                	mov    eax,edx
  40760c:	29 c8                	sub    eax,ecx
  40760e:	83 c0 2a             	add    eax,0x2a
  407611:	89 c2                	mov    edx,eax
  407613:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  407616:	48 98                	cdqe   
  407618:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
