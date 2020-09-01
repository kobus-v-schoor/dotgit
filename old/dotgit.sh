#! /bin/bash
# shellcheck disable=SC2155

# Dotgit is an easy-to-use and effective way to backup all your dotfiles and
# manage them in a repository

# Developer: Kobus van Schoor

declare -r DG_START=0 # Marker for header files
declare -r REPO="$PWD" # Original repo dir
declare -r FILELIST="filelist"
declare -r CRYPTLIST="cryptlist"
declare -r DG_DFDIR="dotfiles"
declare -r DG_DMZ="dmz"
declare -r DG_VERBOSE=$([ "$1" == "verbose" ]; echo -n $?)

function phelp
{
	cat | less <<\EOF
SYNOPSIS:
    Dotgit is an easy-to-use and versatile dotfile manager. It allows you to
    effortlessly move, backup and synchronise your dotfiles between different
    machines. The main ideas that dotgit revolves around are the following:

    - Use a single git repository for ALL your dotfiles (arbitrary amount of
      machines)
    - Straightforward git repo that can be used even when you don't have access
      to dotgit
    - Keep different versions of the same file in the same repo (eg. different
      .bashrc files for different setups) (categories)
    - Easy-to-use commands and setup
    - Do all the heavy-lifting git work (only if you want to)

INITIAL SETUP:
    Firstly create an online git repository (eg. on GitHub). Clone this
    repository to your home folder ('git clone {repo_url} {repo_dest}', check
    online for more details). Next, cd into the repository and run 'dotgit
    init'. Next, setup your dogit repository by editing the filelist as
    explained in the "filelist syntax" section

FILELIST SYNTAX:
    There are only two files inside your dotgit repository that you will be
    editing. They have the names 'filelist' and 'cryptlist'. Both use the same
    syntax and are identical in every way except for the fact that files
    specified inside 'cryptlist' will be encrypted before they are added to the
    repository.

    The filelist uses '#' at the beginning of a line do denominate a comment.
    Blank lines are ignored.

    The filelists use the following syntax:

    file_name:category1,category2

    or simply:

    file_name

    "file_name" can contain spaces and can be any file or folder inside your
    home directory. Categories are a very powerful tool that you can use to
    group files together. If no category is specified it is implicitly added to
    the "common" category. When you specify multiple categories for a single
    file dotgit will link their files together and they will share the exact
    same file. You can also use categories to separate different versions of the
    same file. For example:

    .vimrc:c1,c2
    .vimrc:c3

    In this example categories c1 and c2 will share the same .vimrc and c3 will
    have its own version of .vimrc. Categories can be anything you want it to be
    but its most straight-forward usage is the hostnames of the machines that
    you will be using dotgit on.

    After creating multiple categories it might become tedious to specify them
    all on the command-line, this is where category groups come in. You can
    specify a group with the following syntax:

    group1=category1,category2

    Then, instead of running 'dotgit update category1 category2' every time you
    can just run 'dotgit update group1'. Implicitly added categories (common and
    your hostname) can also be expanded, meaning that if you have a group name
    that matches your hostname it will be expanded for you and you can just run
    'dotgit update'

ENCRYPTION:
    Dotgit has support AES encryption of your dotfiles through PGP. To enable
    encryption of a file simply add the filename to the 'cryptlist' file.

    To incorporate encryption dotgit makes use of a "dmz" folder, a "middle-man"
    folder where all of your encrypted files will be decrypted and from there
    linked to your home folder. This "dmz" folder is inside your repository but
    never added to any of your commits. This also means that whenever you
    make a change to an encrypted dotfile you will have to re-encrypt the file
    (the changes you make will not be automatically added to your repo unlike
    with normal files). To do this you will simply need to cd into your dotfiles
    repository and run 'dotgit encrypt'. More details in the "options" section.

DIRECTORY SUPPORT:
    Dotgit does have support for directories but it is not as versatile and
    forgiving as with normal files as it has a few caveats. Due to the fact that
    dotgit cannot possibly know beforehand what files will reside in a folder it
    needs to determine it at runtime. This means that you will need to take a
    few things in consideration:

    - When running 'dotgit update' all the files in the directory that you want
      there needs to be present (whether they are symlinks to the repo or the
      files themselves). If a file is removed from the folder and you update the
      repository, the file will be removed from the repository as well.
    - When running 'dotgit restore' the destination directory needs to be empty
      or non-existant, otherwise restore will not use the files in the
      repository and remove them.

OPTIONS:
    Usage: dotgit (verbose) [option] (optional categories)

    You can prepend "verbose" to any of the options to enable verbose mode which
    will output dotgit's actions along the way. If you find a problem with
    dotgit please open an issue on github along with this "Verbose" output.

    If you don't add any categories after your option, two categories, "common"
    and your hostname will be implicitly added. When you add categories only the
    files that are in those categories will be taken into consideration. For
    instance, if you specify "c1" after "update" only files marked with the "c1"
    category will be updated. Options with "(ctgs)" after their name support
    categories as a space separated list.

    init           - Setup a new dotgit repository inside the current directory

    update (ctgs)  - Run this after you changed either of your filelists. This
                     will update the repository structures to match your
                     filelists. Do not use this if you only modified your
                     dotfiles, it is unnecessary. If you run dotgit in symlink
                     mode take note that running update will delete the original
                     file inside your home folder and replace it with a link to
                     the repository.

    restore (ctgs) - Run this to create links from your home folder to your
                     repository. You need to run this whenever you want to setup
                     a new machine or if you made changes to the filelists on
                     another machine and you want the changes to be added to the
                     current machine. Take note that dotgit will first remove
                     old links to your dotfiles repository and then create the
                     new links. You will thus need to specify all the categories
                     that you want to restore in one run. When running restore
                     dotgit will automatically try to decrypt your files

    clean          - This will remove all links in your home folder that point
                     to your dotfiles repository

    encrypt        - This will encrypt all the files that you modified since
                     your last encryption. Whenever you modify an encrypted
                     dotfile and want to save the changes to your repository you
                     will need to run this. This will encrypt all files marked
                     for encryption inside the repository.

    decrypt        - This will decrypt all files inside your repository and
                     overwrite the version inside your "dmz" folder. You should
                     run decrypt after pulling in new changes from a remote.
                     This will decrypt all files marked for encryption inside
                     the repository.

    passwd         - Change your dotgit password.

    diff           - This will print your current changes in your dotfiles
                     repository as well as unencrypted changes. Please note that
                     this will not show unencrypted files that were deleted.

    generate       - This will generate a git commit message and push to a
                     remote if it can find one

    help           - Show this message

    'update', 'restore' and the 'clean' option have a 'hard' mode, activated by
    prepending 'hard-' to the option, eg. 'hard-update'. When in this mode
    dotgit will copy the files to/from the repository rather than symlinking it.
    In the case of 'clean' it will also remove files and not just symlinks. This
    can be useful if you want to for example clone the repository onto a
    machine, restore your dotfiles and then delete the repository again.
EOF
}

function errecho
{
	>&2 echo -e "$*"
}

function verecho
{
	[[ $DG_VERBOSE -eq 0 ]] && echo -e "$*"
}

function levecho
{
	local tmp=
	while [[ ${#tmp} -lt "$1" ]]; do
		tmp=$(echo -n "$tmp ")
	done
	tmp=$(echo -n "$tmp>")

	shift
	echo -n "$tmp $*"
}

function prompt
{
	read -rp "$* [Y/n]: " ans

	[[ $ans ==  "Y" ]] && return 0
	[[ $ans ==  "y" ]] && return 0
	[[ ! $ans  ]] && return 0

	return 1
}

function init
{
	if ! cd "$REPO"; then
		errecho "Unable to enter repo."
		exit 1
	fi

	touch "$FILELIST"
	touch "$CRYPTLIST"
	if [ ! -f .gitignore ] || ! grep -q "$DG_DMZ" .gitignore; then
		echo "$DG_DMZ" >> .gitignore
	fi

	if [ ! -d ".git" ]; then
		git init
		git checkout -b master
		git add --all
	fi

	git diff --staged --quiet || git commit -m "Initial dotgit commit" || \
		errecho "Failed to create initial commit, please re-init this" \
		"repository after fixing the errors"
}

function safety_checks
{
	if [[ $REPO == "$HOME" ]]; then
		errecho "Do not run dotgit in your home directory, run it in your" \
			"dotfiles repository"
		exit 1
	fi

	if [ ! -d ".git" ]; then
		errecho "This does not appear to be a git repository. Aborting..."
		exit 1
	fi

	if [ ! -f "$FILELIST" ]; then
		errecho "Cannot locate filelist. Please make sure this repository" \
			"was initialised by dotgit."
		exit 1
	fi

	if [ ! -f "$CRYPTLIST" ]; then
		errecho "Cannot locate cryptlist. Please make sure this repository" \
			"was initialised by dotgit."
		exit 1
	fi

	if ! mkdir -p "$REPO/$DG_DFDIR"; then
		"Unable to create dotfiles dir"
		exit 1
	fi

	if ! mkdir -p "$REPO/$DG_DMZ"; then
		"Unable to create dmz dir"
		exit 1
	fi
}

function init_flists
{
	verecho "\nInitiating filelists"
	# shellcheck disable=SC2164
	cd "$HOME"
	local n=0

	FN=()
	FC=()
	FE=()

	IFS=$'\n'
	for cur in "$REPO/$FILELIST" "$REPO/$CRYPTLIST"; do
		while read -r line; do
			[ ! "$line" ] && continue
			[[ $line =~ ^# ]] && continue
			# shellcheck disable=SC1001
			[[ $line =~ \= ]] && continue

			local -a l
			IFS=$':' l=($line)

			local -a arr
			IFS=$',' arr=(${l[1]:-"common"})
			IFS=$'\n' arr=($(sort -u<<<"${arr[*]}"))

			# If file entry is folder inside repo and home folder has no such
			# file, folder or the folder is empty - then use repo contents as
			# filelist
			if [ -d "$REPO/$DG_DFDIR/${arr[0]}/${l[0]}" ]; then
				if [ ! -f "${l[0]}" ]; then
					if [ ! -d "${l[0]}" ] || [[ ! $(ls -A "${l[0]}") ]]; then
						verecho "$(levecho 1 "Using repo dir for ${l[0]}")"
						PRE="$REPO/$DG_DFDIR/${arr[0]}/"
						mkdir -p "${l[0]}"
					fi
				fi
			fi

			if [ ! -d "${l[0]}" ]; then
				FN+=("${l[0]}")
				IFS=$',' FC+=("${arr[*]}")
				FE+=($n)
				verecho "$(levecho 1 "Added ${l[0]} - ${arr[*]} - $n")"
			else
				IFS=$','
				verecho "$(levecho 1 \
					"Using directory mode for ${l[0]} - ${arr[*]} - $n")"

				IFS=$'\n'
				while read -r fls; do
					[[ ! $fls ]] && continue
					[[ $PRE ]] && fls=${fls#$PRE}
					FN+=("$fls")
					IFS=$',' FC+=("${arr[*]}")
					FE+=($n)
					verecho "$(levecho 2 "Added $fls")"
				done <<< "$(find "$PRE${l[0]}" -not -type d)"
				unset fls
			fi

			unset PRE
		done < "$cur"
		n=1
	done

	IFS=$'\n'
	for i1 in $(seq 0 $((${#FN[@]} - 1))); do
		IFS=$'\n'
		for i2 in $(seq $((i1 + 1)) $((${#FN[@]} - 1))); do
			if [[ ${FN[$i2]} == "${FN[$i1]}" ]]; then
				local f1=0
				local f2=0
				IFS=$','

				for c1 in ${FC[$i1]}; do
					# shellcheck disable=SC2153
					for c2 in "${CTG[@]}"; do
						if [[ $c1 ==  "$c2" ]]; then
							f1=1
							break;
						fi
					done
					[[ $f1 -eq 1 ]] && break
				done

				for c1 in ${FC[$i2]}; do
					for c2 in "${CTG[@]}"; do
						if [[ $c1 ==  "$c2" ]]; then
							f2=1
							break;
						fi
					done
					[[ $f2 -eq 1 ]] && break
				done

				unset c1
				unset c2

				if [[ $f1 -eq 1 ]] && [[ $f2 -eq 1 ]]; then
					IFS=$'\n'
					errecho "Duplicate file entry found:" \
						"${FN[$i1]}:${FC[$i1]}" \
						"${FN[$i2]}:${FC[$i2]}"
					exit 1
				fi
			fi
		done
		unset i2
	done
	unset i1

	unset line
	unset cur
}

function init_cgroups
{
	IFS=$'\n'
	for cur in "$REPO/$FILELIST" "$REPO/$CRYPTLIST"; do
		IFS=$'\n'
		while read -r line; do
			[ ! "$line" ] && continue
			[[ $line =~ ^# ]] && continue
			# shellcheck disable=SC1001
			! [[ $line =~ \= ]] && continue

			IFS=$'='
			local l=($line)
			# shellcheck disable=SC2034
			CTGG[${l[0]}]="${l[1]}"
		done < "$cur"
	done

	unset line
	unset cur
}

function update
{
	[[ $1 == "sym" ]] && clean_home_fast

	# shellcheck disable=SC2155
	verecho "\nEntering update"

	local f
	local -a c
	local e
	IFS=$'\n'
	for index in $(seq 1 ${#FN[@]}); do
		index=$((index - 1))

		f=${FN[$index]}
		IFS=$','
		c=(${FC[$index]})
		e=${FE[$index]}

		local DFDIR

		if [[ $e -eq 1 ]]; then
			DFDIR=$DG_DMZ
		else
			DFDIR=$DG_DFDIR
		fi

		verecho "$(levecho 1 "Updating \"$f\" - ${c[*]} - $e")"

		local found=0
		for i in "${CTG[@]}"; do
			for k in "${c[@]}"; do
				if [[ $k == "$i" ]]; then
					found=1;
					break;
				fi
			done
			[[ $found -eq 1 ]] && break
		done
		unset i
		unset k

		if [[ $found -ne 1 ]]; then
			verecho "$(levecho 2 "Not in specified categories. Skipping...")"
			continue
		fi

		if [[ ! "$1" == "sym" ]]; then
			# shellcheck disable=SC2164
			cd "$HOME"

			if [ ! -f "$f" ]; then
				verecho "$(levecho 2 "Cannot find file in home folder.")"
				continue
			fi

			for i in "${c[@]}"; do
				verecho "$(levecho 2 "Copying to category $i")"
				mkdir -p "$REPO/$DFDIR/$i"
				cp -p --parents "$f" "$REPO/$DFDIR/$i"
			done
			unset i

			continue
		fi

		found=0
		local -i fsym=0
		local fcat=

		# shellcheck disable=SC2164
		cd "$REPO/$DFDIR"

		local d_rm=0
		local f_rm=0
		for i in "${c[@]}"; do
			[ -d "$i/$f" ] && d_rm=1

			local tmp
			tmp=$(dirname "$i/$f")

			mkdir -p "$tmp" > /dev/null 2>&1 || f_rm=1

			if [[ $d_rm -eq 1 ]] || [[ $f_rm -eq 1 ]]; then
				verecho "$(levecho 2 "Type mismatch, removing repo version")"
				if [[ $d_rm -eq 1 ]]; then
					tmp="$i/$f"
				else
					while [ ! -f "$tmp" ] && [ "$tmp" != "$REPO/$DFDIR" ]; do
						tmp=$(dirname "$tmp")
					done

					if [[ $tmp == "$REPO/$DFDIR" ]]; then
						IFS=$' ' errecho "Type mismatch repo error," \
							"unable to find file causing problems. Aborting..."
						exit 1
					fi
				fi

				verecho "$(levecho 3 "Removing $tmp")"
				rm -rf "$tmp"
			fi

			unset tmp
		done
		unset d_rm
		unset f_rm

		for i in "${c[@]}"; do
			if [ -f "$i/$f" ]; then
				found=1
				fcat=$i
				verecho "$(levecho 2 "Found in $i")"

				if [ -h "$i/$f" ] || [ "$i" != "${c[0]}" ]; then
					verecho "$(levecho 3 "Invalid root file")"
					fsym=1
				fi
				break
			fi
		done
		unset i

		if [ $found -eq 0 ]; then
			verecho "$(levecho 2 "Not found in repo, adding to repo")"

			# shellcheck disable=SC2164
			cd "$HOME"

			if [ ! -f "$f" ]; then
				verecho "$(levecho 3 "Cannot find file in home folder.")"
				continue
			fi

			mkdir -p "$REPO/$DFDIR/${c[0]}"
			cp -p --parents "$f" "$REPO/$DFDIR/${c[0]}"
			verecho "$(levecho 3 "Root file added to repo")"
		elif [[ $fsym -eq 1 ]]; then
			verecho "$(levecho 2 "Finding previous root file")"
			# shellcheck disable=SC2155
			local root=$(readlink -f "$REPO/$DFDIR/$fcat/$f")

			if [ ! -f "$root" ]; then
				verecho "$(levecho 3 "Cannot find root file," \
					"trying to find file in home folder")"
				if [ ! -f "$HOME/$f" ]; then
					verecho "$(levecho "Cannot find file in home folder.")"
					continue
				fi
				root="$HOME/$f"
			fi

			verecho "$(levecho 2 "Creating new root - ${c[0]}")"

			mkdir -p "$(dirname "$REPO/$DFDIR/${c[0]}/$f")"
			rm "$REPO/$DFDIR/${c[0]}/$f" > /dev/null 2>&1
			cp -p "$root" "$REPO/$DFDIR/${c[0]}/$f"

			for i in "${c[@]:1}"; do
				rm "$REPO/$DFDIR/$i/$f" > /dev/null 2>&1
			done
			unset i

			verecho "$(levecho 3 "Root file added to repo")"
		fi

		for i in "${c[@]:1}"; do
			mkdir -p "$(dirname "$REPO/$DFDIR/$i/$f")"
			# Link other categories to "root" file (first in cat arr)
			if [ ! -f "$REPO/$DFDIR/$i/$f" ]; then
				ln -rs "$REPO/$DFDIR/${c[0]}/$f" "$REPO/$DFDIR/$i/$f"
				verecho "$(levecho 3 "Co-category \"$i\" linked to root")"
			fi
		done
		unset i

		verecho "$(levecho 2 "Creating/updating link to repo")"
		if [ -a "$HOME/$f" ] || [ -h "$HOME/$f" ]; then
			rm "$HOME/$f"
		fi
		ln -s "$REPO/$DFDIR/${c[0]}/$f" "$HOME/$f"
	done

	unset index
	clean_repo
}

function restore
{
	[[ $1 == "sym" ]] && clean_home_fast

	crypt "decrypt"

	verecho "\nEntering restore"

	local f
	local -a c
	local e
	IFS=$'\n'
	for index in $(seq 1 ${#FN[@]}); do
		index=$((index - 1))

		f=${FN[$index]}
		IFS=$',' c=(${FC[$index]})
		e=${FE[$index]}

		local DFDIR

		if [[ $e -eq 1 ]]; then
			DFDIR=$DG_DMZ
		else
			DFDIR=$DG_DFDIR
		fi

		verecho "$(levecho 1 "Restoring \"$f\" - ${c[*]} - $e")"

		local found=0
		for i in "${CTG[@]}"; do
			for k in "${c[@]}"; do
				if [[ $k == "$i" ]]; then
					found=1;
					break;
				fi
			done
			[[ $found -eq 1 ]] && break
		done
		unset i
		unset k

		if [[ $found -ne 1 ]]; then
			verecho "$(levecho 2 "Not in specified categories. Skipping...")"
			continue
		fi

		if [ ! -f "$REPO/$DFDIR/${c[0]}/$f" ]; then
			verecho "$(levecho 2 "File not found in repo. Skipping...")"
			continue
		fi

		if [ -f "$HOME/$f" ]; then
			prompt "File \"$f\" exists in home folder, replace?" || continue

			verecho "$(levecho 2 "Removing from home folder")"
			rm "$HOME/$f"
		fi

		mkdir -p "$HOME/$(dirname "$f")"
		local cmd=
		if [[ $1 == "sym" ]]; then
			verecho "$(levecho 3 "Creating symlink in home folder")"
			cmd="ln -s"
		else
			verecho "$(levecho 3 "Creating copy in home folder")"
			cmd="cp -p"
		fi
		eval "$cmd \"$REPO/$DFDIR/${c[0]}/$f\" \"$HOME/$f\""
	done
}

function clean_home_fast
{
	verecho "\nInitiating home cleanup"
	# shellcheck disable=SC2164
	cd "$HOME"

	local del
	for f in "${FN[@]}"; do
		del=0

		[ -h "$f" ] && [[ $(readlink "$f") =~ ^$REPO ]] && del=1
		[[ $1 == "nosym" ]] && [ -f "$f" ] && del=1

		[[ $del -ne 1 ]] && continue

		verecho "Removing \"$f\""
		rm "$f"
	done
}

function clean_repo
{
	verecho "\nInitiating repo cleanup"

	verecho "Cleaning dotfiles folder"
	clean_repo_folder "$DG_DFDIR"
	verecho "Cleaning dmz folder"
	clean_repo_folder "$DG_DMZ"
}

function clean_repo_folder
{
	if ! cd "$REPO/$1"; then
		echo "Unable to enter $1 directory"
		exit 1
	fi

	IFS=$'\n'
	while read -r fl; do
		[ ! "$fl" ] && break

		local c=${fl%%/*}
		local f=${fl#*/}
		f=${f%\.hash}

		local found=0

		local index=0
		for fns in "${FN[@]}"; do
			if [[ $fns == "$f" ]]; then
				IFS=$','
				for cts in ${FC[$index]}; do
					if [[ $cts == "$c" ]]; then
						found=1;
						break;
					fi
				done
				unset cts

				[[ $found -eq 1 ]] && break
			fi

			index=$((index + 1))
		done
		unset fns

		if [[ $found -ne 1 ]]; then
			verecho "$(levecho 1 "Removing $fl")"
			rm "$fl"
		fi

	done <<< "$(find . -not -type d | cut -c 3-)"
	unset fl

	verecho "$(levecho 1 "Removing empty directories")"
	find . -type d -empty -delete
}

declare DG_PASS
declare DG_PASS_FILE="passwd"
declare -r DG_HASH="sha1sum"
declare -i DG_HASH_COUNT=1500

function get_password
{
	# For compatibility with previous version of dotgit
	[[ $DG_PREV_PASS ]] && DG_PASS=$DG_PREV_PASS
	unset DG_PREV_PASS
	# -------------------------------------------------

	if [[ ! $DG_PASS ]]; then
		local mod
		if [ -f "$REPO/$DG_PASS_FILE" ]; then
			mod="your"
		else
			mod="a new"
		fi
		echo -n "Please enter $mod password (nothing will be shown): "

		read -sr DG_PASS
		echo
	fi

	# For compatibility with previous version of dotgit
	if [[ $DG_READ_MANGLE ]]; then
		DG_PREV_PASS=$DG_PASS
		IFS=$'\n'
		# shellcheck disable=SC2162
		read DG_PASS <<< "$DG_PASS"
		return
	fi
	# -------------------------------------------------

	IFS=$' '
	local tmp=$DG_PASS

	local -i i=0
	while [[ $i -lt $DG_HASH_COUNT ]]; do
		tmp=($($DG_HASH <<< "${tmp[0]}"))
		i=$((i + 1))
	done

	if [ -f "$REPO/$DG_PASS_FILE" ]; then
		[[ ${tmp[0]} == "$(cat "$REPO/$DG_PASS_FILE")" ]] && return
		errecho "Incorrect password, exiting..."
		exit 1
	else
		echo -n "${tmp[0]}" > "$REPO/$DG_PASS_FILE"
	fi
}

function change_password
{
	get_password
	crypt "decrypt"
	rm "$REPO/$DG_PASS_FILE"
	get_password
	crypt "encrypt" "force"
}

function crypt
{
	verecho "\nInitiating $1ion"
	local FR_D
	local TO_D

	if [[ $1 == "encrypt" ]]; then
		FR_D="$REPO/$DG_DMZ"
		TO_D="$REPO/$DG_DFDIR"
	else
		FR_D="$REPO/$DG_DFDIR"
		TO_D="$REPO/$DG_DMZ"
	fi

	local f
	local -a c

	IFS=$'\n'
	for index in $(seq 1 ${#FN[@]}); do
		index=$((index - 1))

		[[ ${FE[$index]} -ne 1 ]] && continue

		f=${FN[$index]}
		IFS=$',' c=(${FC[$index]})

		verecho "$(levecho 1 "${1^}ing $f")"

		local df_fl="$REPO/$DG_DFDIR/${c[0]}/$f"
		local dm_fl="$REPO/$DG_DMZ/${c[0]}/$f"

		local fr_fl="$FR_D/${c[0]}/$f"
		local to_fl="$TO_D/${c[0]}/$f"

		local hashed
		local hashfl

		if [ -f "$dm_fl" ]; then
			verecho "$(levecho 2 "Found file in dmz")"
			hashed=$($DG_HASH "$dm_fl")
			hashed=${hashed%% *}
		fi

		if [ -f "$df_fl.hash" ]; then
			verecho "$(levecho 2 "Found file in dotfiles")"
			# shellcheck disable=SC2155
			local hashfl=$(cat "$df_fl.hash")
		fi

		if [ ! "$hashed" ] && [[ $1 == "encrypt" ]]; then
			verecho "$(levecho 2 "File not found in dmz. Skipping")"
			continue
		fi

		if [ ! "$hashfl" ] && [[ $1 == "decrypt" ]]; then
			verecho "$(levecho 2 "File not found in dotfiles. Skipping")"
			continue
		fi

		if [[ $hashed == "$hashfl" ]] && [[ $2 != "force" ]]; then
			verecho "$(levecho 2 "File hashes match. Skipping")"
			continue
		fi

		[ ! "$DG_PASS" ] && get_password

		local gpg_cmd

		[[ $1 == "encrypt" ]] && gpg_cmd="-c"
		[[ $1 == "decrypt" ]] && gpg_cmd="-d"

		if [ -a "$to_fl" ] || [ -h "$to_fl" ]; then
			rm "$to_fl"
			[ -f "$to_fl.hash" ] && rm "$to_fl.hash"
		fi

		mkdir -p "$(dirname "$to_fl")"
		gpg -q --batch --passphrase "$DG_PASS" $gpg_cmd -o "$to_fl" "$fr_fl"
		chmod "$(stat -c %a "$fr_fl")" "$to_fl"

		[[ $1 == "encrypt" ]] && echo -n "$hashed" > "$to_fl.hash"

		for cat in "${c[@]:1}"; do
			local fl="$TO_D/$cat/$f"
			if [ -a "$fl" ] || [ -h "$fl" ]; then
				rm "$fl"
				[ -f "$fl.hash" ] && rm "$fl.hash"
			fi
			mkdir -p "$(dirname "$fl")"
			ln -rs "$to_fl" "$fl"
		done
		unset cat

		unset hashed
		unset hashfl
	done
	unset index

	clean_repo
}


declare -a DG_DIFF_T
declare -a DG_DIFF_F

function init_diff
{
	# shellcheck disable=SC2164
	cd "$REPO"
	git add --all
	IFS=$'\n'

	local fl_ch=0
	local cr_ch=0

	while read -r line; do
		local a=${line%% *}
		local f=${line#* }

		f=${f:1}
		f=${f%\"}
		f=${f#\"}

		[[ $f == "$FILELIST" ]] && fl_ch=1 && continue
		[[ $f == "$CRYPTLIST" ]] && cr_ch=1 && continue
		[[ ! $f =~ ^$DG_DFDIR* ]] && continue
		[[ $f =~ .*\.hash ]] && continue

		case "$a" in
			"A")DG_DIFF_T+=("added");;
			"M")DG_DIFF_T+=("modified");;
			"D")DG_DIFF_T+=("deleted");;
			"R")DG_DIFF_T+=("renamed");;
			"T")DG_DIFF_T+=("typechange");;
			*)errecho "Unknown git change \"$a\" - $f"; continue;;
		esac;

		DG_DIFF_F+=("${f#$DG_DFDIR\/}")
	done <<< "$(git status --porcelain)"
	unset line

	if [[ ${#DG_DIFF_F[@]} -eq 0 ]]; then
		[[ $fl_ch -ne 0 ]] && DG_DIFF_F+=("filelist") && DG_DIFF_T+=("modified")
		[[ $cr_ch -ne 0 ]] && DG_DIFF_F+=("cryptlist") && DG_DIFF_T+=("modified")
	fi

	git reset -q
}

function print_diff
{
	init_diff

	IFS=$'\n'
	for index in $(seq 1 ${#DG_DIFF_T[@]}); do
		index=$((index - 1))
		echo "${DG_DIFF_T[$index]^} ${DG_DIFF_F[$index]}"
	done
	unset index

	local f
	local -a c

	local str
	IFS=$'\n'
	for index in $(seq 1 ${#FN[@]}); do
		index=$((index - 1))

		[[ ${FE[$index]} -ne 1 ]] && continue

		f=${FN[$index]}
		IFS=$',' c=(${FC[$index]})

		for cat in "${c[@]}"; do
			[ ! -f "$REPO/$DG_DMZ/$cat/$f" ] && continue

			if [ ! -f "$REPO/$DG_DFDIR/$cat/$f" ]; then
				str="$str\nAdded $cat/$f"
				continue
			fi

			[ -h "$REPO/$DG_DFDIR/$cat/$f" ] && continue

			local hashed
			local hashfl
			hashed=$($DG_HASH "$REPO/$DG_DMZ/$cat/$f")
			hashed=${hashed%% *}
			hashfl=$(cat "$REPO/$DG_DFDIR/$cat/$f.hash")

			[[ $hashed != "$hashfl" ]] && str="$str\nModified $cat/$f"
		done
		unset cat
	done

	[ "$str" ] && echo -e "\nUnencrypted changes:\n$str"
	unset index
}

function generate_commit_msg
{
	crypt "encrypt"
	init_diff

	local str
	IFS=$'\n'
	for index in $(seq 1 ${#DG_DIFF_T[@]}); do
		index=$((index - 1))
		str="$str; ${DG_DIFF_T[$index]} ${DG_DIFF_F[$index]}"
	done
	unset index

	if git diff --quiet '@{u}..' && [[ ! $str ]]; then
		errecho "No changes to repository"
		exit
	fi

	if [[ $str ]]; then
		str=${str:2}
		str=${str^}

		git add --all
		git commit -m "$str"
	fi

	if [[ $(git remote -v) ]]; then
		if prompt "Remote detected. Do you want to push to remote?"; then
			git push
		fi
	fi
}

declare -a CTG # Active categories
declare -A CTGG # Category groups

declare -a FN # File names
declare -a FC # Normal categories
declare -a FE # File encrypt flag

[[ $DG_VERBOSE -eq 0 ]] && shift

[[ $# -ne 0 ]] && [[ $1 != "init" ]] && [[ $1 != "help" ]] && init_cgroups

declare -a tctg
if [[ $# -eq 0 ]]; then
	phelp
	exit
elif [[ $# -eq 1 ]]; then
	tctg=(common $HOSTNAME)
else
	tctg=(${@:2})
fi

IFS=$' '
for g in "${tctg[@]}"; do
	if [ "${CTGG[$g]}" ]; then
		verecho "Expanding categories with group $g=[${CTGG[$g]}]"
		IFS=$','
		CTG+=(${CTGG[$g]})
	else
		# shellcheck disable=SC2034
		CTG+=($g)
	fi
done

IFS=$'\n' CTG=($(sort -u <<<"${CTG[*]}"))
IFS=$','
verecho "Active categories: ${CTG[*]}"

if [[ $1 != "init" ]] &&  [[ $1 != "help" ]]; then
	safety_checks
	init_flists

	# Check if previous version of dotgit is used
	if [ -f "$REPO/$DG_PASS_FILE" ] && \
		[[ $(stat -c %s "$REPO/$DG_PASS_FILE") -eq 68 ]]; then
		echo "Updating repo to be compatible with new version of dotgit"

		# shellcheck disable=SC2034
		DG_READ_MANGLE=1
		get_password
		crypt "decrypt"
		rm "$REPO/$DG_PASS_FILE"
		unset DG_READ_MANGLE
		get_password
		crypt "encrypt"
	fi

	if [ -f "$REPO/dir_filelist" ]; then
		echo "Migrating dir_filelist"
		cat "$REPO/dir_filelist" >> "$REPO/$FILELIST"
		rm "$REPO/dir_filelist"
	fi

	if [ -f "$REPO/dir_cryptlist" ]; then
		echo "Migrating dir_cryptlist"
		cat "$REPO/dir_cryptlist" >> "$REPO/$CRYPTLIST"
		rm "$REPO/dir_cryptlist"
	fi
fi

case "$1" in
	"help")phelp;;
	"init")init;;
	"update")update "sym";;
	"restore")restore "sym";;
	"clean")clean_home_fast "sym";;
	"hard-update")update "nosym";;
	"hard-restore")restore "nosym";;
	"hard-clean")clean_home_fast "nosym";;
	"encrypt")crypt "encrypt";;
	"decrypt")crypt "decrypt";;
	"passwd")change_password;;
	"diff")print_diff;;
	"generate")generate_commit_msg;;
	*)echo -e "$1 is not a valid argument."; exit 1;;
esac;
