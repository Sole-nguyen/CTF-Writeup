
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

0000000000415292 <.text+0x14162>:
  415292:	f3 0f 1e fa          	endbr64 
  415296:	55                   	push   rbp
  415297:	48 89 e5             	mov    rbp,rsp
  41529a:	48 83 ec 70          	sub    rsp,0x70
  41529e:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  4152a2:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  4152a9:	00 00 
  4152ab:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  4152af:	31 c0                	xor    eax,eax
  4152b1:	c7 45 a4 08 ed 00 00 	mov    DWORD PTR [rbp-0x5c],0xed08
  4152b8:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4152bb:	83 f0 08             	xor    eax,0x8
  4152be:	89 c2                	mov    edx,eax
  4152c0:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4152c3:	83 e0 08             	and    eax,0x8
  4152c6:	01 c0                	add    eax,eax
  4152c8:	01 d0                	add    eax,edx
  4152ca:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4152cd:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4152d0:	83 f0 c6             	xor    eax,0xffffffc6
  4152d3:	89 c2                	mov    edx,eax
  4152d5:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4152d8:	83 e0 c6             	and    eax,0xffffffc6
  4152db:	01 c0                	add    eax,eax
  4152dd:	01 d0                	add    eax,edx
  4152df:	83 c0 01             	add    eax,0x1
  4152e2:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4152e5:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4152e8:	83 c8 49             	or     eax,0x49
  4152eb:	89 c1                	mov    ecx,eax
  4152ed:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4152f0:	83 e0 49             	and    eax,0x49
  4152f3:	89 c2                	mov    edx,eax
  4152f5:	89 c8                	mov    eax,ecx
  4152f7:	29 d0                	sub    eax,edx
  4152f9:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4152fc:	48 b8 e8 c5 c8 8c d5 	movabs rax,0x8cd9c3d58cc8c5e8
  415303:	c3 d9 8c 
  415306:	48 ba c1 c9 cd c2 8c 	movabs rdx,0x8cc3d88cc2cdc9c1
  41530d:	d8 c3 8c 
  415310:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  415314:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  415318:	48 b8 c8 c3 8c d8 c4 	movabs rax,0x93d8cdc4d88cc3c8
  41531f:	cd d8 93 
  415322:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  415326:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  41532d:	eb 31                	jmp    415360 <stderr@GLIBC_2.2.5-0x3acc0>
  41532f:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  415332:	48 98                	cdqe   
  415334:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  415339:	83 c8 ac             	or     eax,0xffffffac
  41533c:	89 c2                	mov    edx,eax
  41533e:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  415341:	48 98                	cdqe   
  415343:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  415348:	83 e0 ac             	and    eax,0xffffffac
  41534b:	89 c1                	mov    ecx,eax
  41534d:	89 d0                	mov    eax,edx
  41534f:	29 c8                	sub    eax,ecx
  415351:	89 c2                	mov    edx,eax
  415353:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  415356:	48 98                	cdqe   
  415358:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  41535c:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  415360:	83 7d a8 17          	cmp    DWORD PTR [rbp-0x58],0x17
  415364:	7e c9                	jle    41532f <stderr@GLIBC_2.2.5-0x3acf1>
  415366:	c6 45 e8 00          	mov    BYTE PTR [rbp-0x18],0x0
  41536a:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
  41536e:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  415371:	0f be c0             	movsx  eax,al
  415374:	83 c0 01             	add    eax,0x1
  415377:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  41537a:	eb 3c                	jmp    4153b8 <stderr@GLIBC_2.2.5-0x3ac68>
  41537c:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  41537f:	83 e0 01             	and    eax,0x1
  415382:	85 c0                	test   eax,eax
  415384:	75 07                	jne    41538d <stderr@GLIBC_2.2.5-0x3ac93>
  415386:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  415389:	d1 e8                	shr    eax,1
  41538b:	eb 21                	jmp    4153ae <stderr@GLIBC_2.2.5-0x3ac72>
  41538d:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  415390:	89 d0                	mov    eax,edx
  415392:	01 c0                	add    eax,eax
  415394:	01 d0                	add    eax,edx
  415396:	83 f0 fe             	xor    eax,0xfffffffe
  415399:	89 c1                	mov    ecx,eax
  41539b:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  41539e:	89 d0                	mov    eax,edx
  4153a0:	01 c0                	add    eax,eax
  4153a2:	01 d0                	add    eax,edx
  4153a4:	83 e0 fe             	and    eax,0xfffffffe
  4153a7:	01 c0                	add    eax,eax
  4153a9:	01 c8                	add    eax,ecx
  4153ab:	83 c0 01             	add    eax,0x1
  4153ae:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  4153b1:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4153b4:	85 c0                	test   eax,eax
  4153b6:	74 08                	je     4153c0 <stderr@GLIBC_2.2.5-0x3ac60>
  4153b8:	83 7d ac 01          	cmp    DWORD PTR [rbp-0x54],0x1
  4153bc:	75 be                	jne    41537c <stderr@GLIBC_2.2.5-0x3aca4>
  4153be:	eb 01                	jmp    4153c1 <stderr@GLIBC_2.2.5-0x3ac5f>
  4153c0:	90                   	nop
  4153c1:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  4153c5:	48 89 c7             	mov    rdi,rax
  4153c8:	e8 e3 bc fe ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  4153cd:	bf 01 00 00 00       	mov    edi,0x1
  4153d2:	e8 39 bd fe ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  4153d7:	f3 0f 1e fa          	endbr64 
  4153db:	55                   	push   rbp
  4153dc:	48 89 e5             	mov    rbp,rsp
  4153df:	48 83 ec 60          	sub    rsp,0x60
  4153e3:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  4153e7:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  4153ee:	00 00 
  4153f0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  4153f4:	31 c0                	xor    eax,eax
  4153f6:	c7 45 b8 0c 69 00 00 	mov    DWORD PTR [rbp-0x48],0x690c
  4153fd:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  415400:	83 f0 bc             	xor    eax,0xffffffbc
  415403:	89 c2                	mov    edx,eax
  415405:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  415408:	83 e0 bc             	and    eax,0xffffffbc
  41540b:	01 c0                	add    eax,eax
  41540d:	01 d0                	add    eax,edx
  41540f:	83 c0 01             	add    eax,0x1
  415412:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  415415:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  415418:	83 f0 db             	xor    eax,0xffffffdb
  41541b:	89 c2                	mov    edx,eax
  41541d:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  415420:	83 e0 db             	and    eax,0xffffffdb
  415423:	01 c0                	add    eax,eax
  415425:	01 d0                	add    eax,edx
  415427:	83 c0 01             	add    eax,0x1
  41542a:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  41542d:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  415430:	35 13 ff ff ff       	xor    eax,0xffffff13
  415435:	89 c2                	mov    edx,eax
  415437:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  41543a:	24 13                	and    al,0x13
  41543c:	01 c0                	add    eax,eax
  41543e:	01 d0                	add    eax,edx
  415440:	83 c0 01             	add    eax,0x1
  415443:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  415446:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  415449:	34 b3                	xor    al,0xb3
  41544b:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  41544e:	48 b8 fa f9 eb f0 a2 	movabs rax,0xe1ebb8a2f0ebf9fa
  415455:	b8 eb e1 
  415458:	48 ba f6 ec f9 e0 b8 	movabs rdx,0xeaeafdb8e0f9ecf6
  41545f:	fd ea ea 
  415462:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  415466:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  41546a:	66 c7 45 d0 f7 ea    	mov    WORD PTR [rbp-0x30],0xeaf7
  415470:	c7 45 bc 00 00 00 00 	mov    DWORD PTR [rbp-0x44],0x0
  415477:	eb 30                	jmp    4154a9 <stderr@GLIBC_2.2.5-0x3ab77>
  415479:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  41547c:	48 98                	cdqe   
  41547e:	0f b6 54 05 c0       	movzx  edx,BYTE PTR [rbp+rax*1-0x40]
  415483:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  415486:	48 98                	cdqe   
  415488:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  41548d:	83 e0 98             	and    eax,0xffffff98
  415490:	8d 0c 00             	lea    ecx,[rax+rax*1]
  415493:	89 d0                	mov    eax,edx
  415495:	29 c8                	sub    eax,ecx
  415497:	83 e8 68             	sub    eax,0x68
  41549a:	89 c2                	mov    edx,eax
  41549c:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  41549f:	48 98                	cdqe   
  4154a1:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  4154a5:	83 45 bc 01          	add    DWORD PTR [rbp-0x44],0x1
  4154a9:	83 7d bc 11          	cmp    DWORD PTR [rbp-0x44],0x11
  4154ad:	7e ca                	jle    415479 <stderr@GLIBC_2.2.5-0x3aba7>
  4154af:	c6 45 f2 00          	mov    BYTE PTR [rbp-0xe],0x0
  4154b3:	48 8b 55 a8          	mov    rdx,QWORD PTR [rbp-0x58]
  4154b7:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  4154bb:	48 89 c6             	mov    rsi,rax
  4154be:	48 8d 05 82 eb 02 00 	lea    rax,[rip+0x2eb82]        # 444047 <stderr@GLIBC_2.2.5-0xbfd9>
  4154c5:	48 89 c7             	mov    rdi,rax
  4154c8:	b8 00 00 00 00       	mov    eax,0x0
  4154cd:	e8 0e bc fe ff       	call   4010e0 <stderr@GLIBC_2.2.5-0x4ef40>
  4154d2:	bf 7f 00 00 00       	mov    edi,0x7f
  4154d7:	e8 34 bc fe ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  4154dc:	f3 0f 1e fa          	endbr64 
  4154e0:	55                   	push   rbp
  4154e1:	48 89 e5             	mov    rbp,rsp
  4154e4:	48 83 c4 80          	add    rsp,0xffffffffffffff80
  4154e8:	48 89 7d 88          	mov    QWORD PTR [rbp-0x78],rdi
  4154ec:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  4154f3:	00 00 
  4154f5:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  4154f9:	31 c0                	xor    eax,eax
  4154fb:	c7 45 98 3e c3 00 00 	mov    DWORD PTR [rbp-0x68],0xc33e
  415502:	8b 45 98             	mov    eax,DWORD PTR [rbp-0x68]
  415505:	0c b3                	or     al,0xb3
  415507:	89 c2                	mov    edx,eax
  415509:	8b 45 98             	mov    eax,DWORD PTR [rbp-0x68]
  41550c:	25 b3 00 00 00       	and    eax,0xb3
  415511:	01 d0                	add    eax,edx
  415513:	89 45 98             	mov    DWORD PTR [rbp-0x68],eax
  415516:	8b 45 98             	mov    eax,DWORD PTR [rbp-0x68]
  415519:	0c a0                	or     al,0xa0
  41551b:	89 c1                	mov    ecx,eax
  41551d:	8b 45 98             	mov    eax,DWORD PTR [rbp-0x68]
