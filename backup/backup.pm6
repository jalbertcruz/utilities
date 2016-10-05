#!/home/j/appslnx/rakudo-star-2016.07/install/bin/perl6


# my @concrete_paths = ();

# my $prefix = '/home/j/Downloads/aa/';
# my $destination = '/home/j/Downloads/aa/result/';

# my @paths = 'bower_components/summernote/dist/', 'bower_components/knockout/';


my $home_backup = 1 == 1;

my @concrete_paths = ();
my $excluded_paths = set('src/dbs/',);
my $prefix = '/home/j/';
my $destination = '/run/media/j/Medias/BFS/10-16/home/';
my @init_paths = '.android/', '.AndroidStudio2.2/', 'appslnx/google/', 'appslnx/jetbrains/', 'code/', '.config/git/',
                  'Desktop/', 'Downloads/', '.m2/', '.lein/', '.ivy2/', '.gradle/', '.mozilla/',
                  '.npm/', '.sbt/', 'src/', '.ssh/', '.vim/', '.zprezto/', '.emacs.d/', '.pub-cache/',;
my @just_files = '.zhistory', '.viminfo', '.spacemacs', '.gitconfig', '.bash_history',
                 '.tmux.conf', '.vimrc', '.bashrc',;


if ! $home_backup {
    @concrete_paths = 'Literature/', 'ff/',;
    $excluded_paths = set();
    $prefix = '/home/datos/';
    $destination = '/run/media/j/Medias/BFS/10-16/d/';
    @init_paths = 'docs/', 'docs/P/PLs/Varied/', 'docs/P/PLs/Varied/C#/Basics/', 'docs/SWE/',
                  'docs/AI/', 'docs/OSs/', 'mdocs/', 'mdocs/teaching/', 'mdocs/docencia/Postgrados/', 'installers/',;
    @concrete_paths = 'ff/',;
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
