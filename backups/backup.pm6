#!/home/a/rakudo/bin/perl6
#!/home/j/appslnx/rakudo-star-2016.07/install/bin/perl6


# my @concrete_paths = ();

# my $prefix = '/home/j/Downloads/aa/';
# my $destination = '/home/j/Downloads/aa/result/';

# my @paths = 'bower_components/summernote/dist/', 'bower_components/knockout/';


my $home_backup = 1 == 1;

my @concrete_paths = ();
my $excluded_paths = set('src/dbs/',);
my $prefix = '/home/a/';
my $destination = '/media/a/Medias/BFS/1904/h/';
my @init_paths = 'appslnx/google/', 'appslnx/jetbrains/', '.config/git/',
                  'Desktop/', 'Downloads/', '.lein/', '.ivy2/', '.mozilla/',
                  '.sbt/', 'src/', '.ssh/', '.vim/', '.zprezto/', '.virtualenvs/',
                  '.emacs.d/', '.toolsconfig/', 
                  #'Android', 
                  ;
my @just_files = '.zhistory', '.viminfo', '.spacemacs', '.gitconfig', '.bash_history',
                 '.tmux.conf', '.vimrc', '.bashrc',;


if ! $home_backup {
    @concrete_paths = 'ff/', 'history/',;
    $excluded_paths = set();
    $prefix = '/media/a/data/';
    $destination = '/media/a/Medias/BFS/1904/d/';
    @init_paths = 'docs/', 
                  'docs-files/P/PLs/Scala/src/akka/akka-http/', 
                  'docs-files/P/PLs/Scala/src/akka/akka/',
                  'docs-files/P/PLs/Clojure/src/', 
                  #'docs/P/PLs/varied/', 'docs/SWE/',
                  'docs/AI/', 'docs/OSs/', 'mdocs/', 'docs/teaching/', 
                  'mdocs/docencia/Postgrados/', 'repo/internet/',;
    # @concrete_paths = 'ff/',;
    @just_files = ();
}

my $all_paths = set(@init_paths);

if ! $home_backup {
    my @all_paths = ();
    for @init_paths -> $p {
        my @l = $p.split('/')[0..*-2];
        for 0..(@l.elems-1) -> $i {
            @all_paths.push(@l[0..$i]);
        }
    }
    $all_paths = set(
        (for @all_paths -> $a { "$a.join('/')/" })
    );
}


chdir $prefix;

if $home_backup {
    for (grep {! "$destination$_".IO.e}, @just_files) -> $f {
        say "cp $f $destination";
        run 'cp', $f, $destination;
    }
}

for @concrete_paths -> $p {
    my $new_tar = "$destination$p.substr(0, *-1).tar";
    if ! $new_tar.IO.e {
        run 'tar', '-cvf', $new_tar, $p
    }
}

my $full_paths = Set.new((for $all_paths.keys -> $x { "$prefix$x" }));

for $all_paths.keys -> $p {
    my $current_target_path = "$destination$p";
    mkdir $current_target_path if ! $current_target_path.IO.e;
    my $new_dir = "$prefix$p";
    chdir $new_dir;

    for (grep { $_.IO.d }, dir) -> $e {
        if "$new_dir$e/" !(elem) $full_paths {
            my $new_tar = "$current_target_path$e.tar";
            if ((! $new_tar.IO.e) and ("$p$e/" !(elem) $excluded_paths)) {
                run 'tar', '-cvf', $new_tar, $e
            }
        }
    }

    for (grep { $_.IO.f and ! "$current_target_path$_".IO.e }, dir) -> $e {
        say "cp $e $current_target_path";
        run 'cp', $e, "$current_target_path"
    }

}
