#!/home/j/appslnx/rakudo-star-2016.07/install/bin/perl6

my @concrete_paths = ();

my $prefix = '/home/j/Downloads/aa/';
my $destination = '/home/j/Downloads/aa/result/';

my @paths = 'bower_components/summernote/dist/', 'bower_components/knockout/';

my @extended_paths = ();

for @paths -> $p {
    my @l = $p.split('/')[0..*-2];
    for 0..(@l.elems-1) -> $i {
        @extended_paths.push(@l[0..$i]);
    }
}

my $extended_paths = Set.new((for @extended_paths -> $a { $a.join('/') }));

chdir $prefix;

my $full_paths = Set.new((for $extended_paths.keys -> $x { "$prefix$x" }));

for $extended_paths.keys -> $p {
    my $np = "$destination$p";
    mkdir $np;
    chdir "$prefix$p";
    for (grep { $_.IO.d }, dir) -> $d {
        if "$prefix$p/$d" !(elem) $full_paths and
           ! "$destination$p$d.tar".IO.e {
               run 'tar', '-cf', "$destination$p/$d.tar", $d
        }
    }

    for (grep { $_.IO.f }, dir) -> $f {
        if ! "$destination$p/$f".IO.e {
            run 'cp', $f, "$destination$p"
        }
    }
}
