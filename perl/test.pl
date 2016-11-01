#!/usr/bin/env perl

use strict;
use warnings;

my $filename = '../logs/testfile';
open(my $fh, '<:encoding(UTF-8)', $filename)
	or die "could not open file '$filename' $!";

sub print_filter {
	my $row = shift;
	return unless ($row =~ m/(data)/);
	print "$row\n";
}

while (my $row = <$fh>) {
	chomp $row;
	print_filter($row);
	#if ($row =~ /data/) {
	#	print "$row\n";
#	}
}
