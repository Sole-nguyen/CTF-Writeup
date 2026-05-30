#!/usr/bin/perl -w 

use strict;
use warnings;
use IO::Handle;
STDOUT->autoflush(1); # Enable autoflush for STDOUT
close STDERR; # There is no error as a long as you don't see them #bigbrain

# Read the flag but only a H3cker could get it!
open(my $fh, '<', "flag.txt");
my $flag = <$fh>;
close($fh);

# Cool banner
print '
 $$$$$$\                           $$$$$$\                                $$\                     
$$  __$$\                         $$  __$$\                               \__|                    
$$ /  \__|$$\   $$\ $$$$$$\$$$$\  $$ /  \__| $$$$$$\   $$$$$$\ $$\    $$\ $$\  $$$$$$$\  $$$$$$\  
\$$$$$$\  $$ |  $$ |$$  _$$  _$$\ \$$$$$$\  $$  __$$\ $$  __$$\\\$$\  $$  |$$ |$$  _____|$$  __$$\ 
 \____$$\ $$ |  $$ |$$ / $$ / $$ | \____$$\ $$$$$$$$ |$$ |  \__|\$$\$$  / $$ |$$ /      $$$$$$$$ |
$$\   $$ |$$ |  $$ |$$ | $$ | $$ |$$\   $$ |$$   ____|$$ |       \$$$  /  $$ |$$ |      $$   ____|
\$$$$$$  |\$$$$$$  |$$ | $$ | $$ |\$$$$$$  |\$$$$$$$\ $$ |        \$  /   $$ |\$$$$$$$\ \$$$$$$$\ 
 \______/  \______/ \__| \__| \__| \______/  \_______|\__|         \_/    \__| \_______| \_______|

';

while (1) {
  print "Enter a number to sum with 42: ";
  my $string = <STDIN>;
  chomp $string;
  my $result = eval "42 + " . $string;
  print "Result: " . $result . "\n";
}
