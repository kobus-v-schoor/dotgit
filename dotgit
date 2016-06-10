#! /bin/bash

# Dotgit is an easy-to-use and effective way to backup all your dotfiles and
# manage them in a repository

# Developer: Kobus van Schoor

REPO="$PWD"
NORMFILES=""
CRYPTFILES=""
DOTFILES=""
DMZ=""
PASSWD=""

function cfilelist
{
	NORMFILES=$(grep -v '^#' "$REPO/filelist" | grep -v "^$" | awk '!a[$0]++')
	CRYPTFILES=$(grep -v '^#' "$REPO/cryptlist" | grep -v "^$" | awk '!a[$0]++')
	DOTFILES="$REPO/dotfiles"
	DMZ="$REPO/dmz"
}

function phelp
{
	echo 'Usage: dotgit [option] (optional args)

  To make a new dotgit repository first create your online repository, and then
  clone it onto your target host (git clone {repo_url} {repo_dest}). Go into
  your repository and then run dotgit init inside of it. The repository will
  then be ready to be used with dotgit.

  If you already have a dotgit repository and would like to use it on another
  host, simply clone the repository onto the target host and the repository will
  be ready to use with dotgit.

Filelist syntax:
  .bashrc             --  Will be in "common" folder and will be restored to
                          home folder, regardless of hostname (unless category
                          is specified)
  .vimrc:host1,host2  --  Will only be restored if hostname of machine matches
                          "host1" or "host2"
  .vimrc:host3        --  Will be kept seperate from .vimrc above and will only
                          be restored on host3
  .xinitrc:category1  --  When category1 is specified as category only files
                          with category1 suffix will be restored (or backed up)
                          (also excludes common folder)

  Categories and host use exactly the same syntax. This also means that you can
  specify a file to belong to multiple categories (and keep them synced)
  Comments are indicated with a # at the begining of the line, comments at the
  end of a line is not yet supported

  After making any changes to the filelist you should run dotgit update, commit
  and push your changes and then run dotgit restore on all other hosts you use
  This ensures that the symlinking hierarchy stays up-to-date

USE COPYING INSTEAD OF SYMLINKING:
  If you prefer not to use symlinks in your home dir (eg. if the repo will not
  live on on the host or because of special filesystem setups) you have two
  options. If you only want to copy the dotfiles once you can use the "hard"
  versions of the various operations described below. If you want a long-term
  solution simply add a file named "hard" to the root of your dotgit repo (file
  can be empty). This will cause dotgit to simply invoke the "hard" versions of
  the operation automatically when using their normal couterparts (eg "dotgit
  restore" will now be equivalent to "dotgit hard-restore"). To see what
  operations will be affected by this option see below.

ENCRYPTION:
  AES encryption is supported by dotgit in both symlinking and "hard" mode. To
  set up encryption just put the relevant filenames in the "cryptlist" file in
  the root of the dotgit repo. The "cryptlist" file uses exactly the same syntax
  as the normal filelist.

  Unlike with the the unencrypted files encrypted files can''t be updated to the
  repository automatically. They first need to be encrypted before they can be
  commited and pushed to a remote. Because of this when linking or copying the
  dotfiles to your home dir the encrypted files will first be decrypted and then
  put in the "dmz" folder of dotgit. Inside this folder they are decrypted and
  these files will be linked into your home dir. When you wan''t to commit your
  changes to the repository these files will have to encrypted first and then
  copied back into the repository. Automatic decryption can be done with git
  hooks, so when you do a ''git pull'' the new files will be decrypted
  automatically. New files will also be automatically encrypted when you run
  ''dotgit generate''.

  NOTE: When cloning a dotgit repo, you will first need to run ''dotgit init''
  inside the repo to set up the git hooks as they cannot be stored inside the
  repo when pushed to a remote.

OPTIONS:
  If an argument is passed to the relevant functions only files pertaining to
  that category or hostname will be taken into account (if an argument is
  supplied the "common" files will also be ignored)

  update (arg)        --  If new files are added to the filelist, copy them to
                          the repository and set up links in home folder
                          If any changes are made to the filelist you should run
                          dotgit with the update option to keep symlinks
                          up-to-date.
                          "Hard" option - Will copy files into repository and
                          leave the files in the home dir intact.

  restore (arg)       --  Set up links in home folder to repository.
                          "Hard" option - Same as hard-restore.

  generate            --  Encrypt necessary files, generate a commit message,
                          commit changes and push to remote.

  hard-restore (arg)  --  Make a copy from the dotgit repository into home dir
                          NOTE: This will overwrite existing files without
                          confirmation

  passwd              --  If no password has been set, set new password. If
                          there is already a password set, change password

  encrypt             --  Encrypt all files currently in the dmz folder and put
                          them in the dotfiles folder. This is neccesary when
                          changes were made to files that are stored encrypted
                          in the repo. This needs to be run if you are making
                          commits manually but not if you use the "generate"
                          operation. See "generate" for details.

  decrypt             --  Decrypt all encrypted files in the repository. If the
                          local "dmz" version differs from the decrypted version
                          you will be given a choice of which file to keep

  clean               --  Delete all links in your home dir that refers to this
                          dotgit repo

  init                --  Initialize current folder with new dotgit repo or if
                          it is already initialized as a dotgit repo, setup git
                          hooks that will automatically decrypt files after a
                          git pull or merge

  diff                --  Show what files changed from previous commit in dotgit
                          repository

  help                --  Show this message'
}

function safeguards
{
	if [ $1 == "init" ] || \
		[ $1 == "diff" ] || \
		[ $1 == "help" ]; then
		return
	fi

	echo "Running safeguards..."

	if [ "$REPO" == "$HOME" ]; then
		echo "You shouldn't run this in your home folder, make a seperate" \
		"folder for your dotfiles"
		ext
	fi

	if [ ! -f "$REPO/filelist" ]; then
		echo "Filelist not found. Aborting..."
		ext
	fi

	if [ ! -f "$REPO/cryptlist" ]; then
		echo "Cryptlist not found. If this is a valid dotgit repo it is"\
			"possible that this repo just has not been initialized again to"\
			"support the new encryption. Please run 'dotgit init', this should"\
			"resolve the error. Please also read the help message for further"\
			"instructions regarding encryption. Aborting..."
		ext
	fi

	if [ ! -d "$REPO/.git" ]; then
		echo "This does not seem to be a git repository. Aborting..."
		ext
	fi

	if grep -q "//" "$REPO/filelist"; then
		echo "Converting filelist to new comment syntax (// -> #)..."
		sed -i "s/\/\//#/g" "$REPO/filelist"
	fi

	if [ ! -d "$REPO/dotfiles" ]; then
		echo "Dotfiles folder not found. Aborting..."
		ext
	fi

	if grep "#--hard--" "$REPO/filelist" > /dev/null; then
		echo "Converting 'hard' option to new syntax. Please read help message"\
			"for further details"
		grep -v "#--hard--#" "$REPO/filelist" > "$REPO/tmp"
		mv "$REPO/tmp" "$REPO/filelist"
	fi

	OLDIFS=$IFS
	IFS=$(echo -en '\n\b')

	for i in $(grep -v "^#" "$REPO/filelist" | grep -v '^$'); do
		if echo "$i" | grep -qv ":"; then
			if grep "$i" "$REPO/cryptlist" | grep -qv ":"; then
				echo "Duplicate filelist/cryptlist entry found ($i)."\
					"Aborting..."
				ext
			fi
		else
			ownrs=($(echo $i | rev | sed 's/\:.*//' | sed 's/\,/\n/g' | rev))
			filename=$(echo $i | sed 's/\:.*//')
			for i in $ownrs; do
				if grep "$filename" "$REPO/cryptlist" | grep ":" | grep -q "$i";
				then echo "Duplicate filelist/cryptlist entry found"\
					"($filename). Aborting..."
					ext
				fi
			done
		fi
	done
	IFS=$OLDIFS
}

function pstatus
{
	type="Adding"
	if [ -n "$3" ]; then
		type="$3"
	fi;

	printf "%-15s" "-->$type"; printf "%-20s" $2 $1; printf "\n"
}

function pprompt
{
	if [ ! -f "$REPO/passwd" ]; then
		echo "Password hash not found - please create one with dotgit passwd."\
			"Aborting..."
		ext
	fi

	echo -n "Please enter a password for $1 (nothing will be shown): "
	stty -echo
	read ans
	stty echo
	echo ""
	if [ "$(echo $ans | sha1sum)" != "$(cat "$REPO/passwd")" ]; then
		echo "Incorrect password. Aborting..."
		ext
	fi
	PASSWD=1
	touch "$REPO/tmp"
	chmod 600 "$REPO/tmp"
	echo "$ans" > "$REPO/tmp"
}

function passwd
{
	if [ ! -f "$REPO/passwd" ]; then
		echo "The password you enter here will be hashed (SHA1) en then stored
inside your repository to be used to ensure that you use the same password
between runs"

		echo -e "\nPasswords will not be shown\n"
		stty -echo

		echo -n "Please enter password to be used for encryption/decryption: "
		read ans
		echo ""
		echo -n "Please verify password: "
		read ans2
		echo ""
		stty echo

		if [ "$ans" != "$ans2" ]; then
			echo "Passwords do no match, aborting..."
			stty echo
			ext
		fi

		touch "$REPO/tmp"
		chmod 600 "$REPO/tmp"
		echo "$ans" > "$REPO/tmp"
		echo "$ans" | sha1sum > "$REPO/passwd"
	else
		echo -e "\nPasswords will not be shown\n"
		stty -echo

		echo -n "Please enter current password: "
		read ans
		echo ""
		hash=$(echo $ans | sha1sum)

		if [ "$hash" != "$(cat "$REPO/passwd")" ]; then
			echo "Incorrect password, aborting..."
			stty echo
			ext
		fi

		PASSWD=1
		echo "$ans" > "$REPO/tmp"
		decrypt

		echo -n "Please enter new password to be used for"\
			"encryption/decryption:"
		read ans
		echo ""
		echo -n "Please verify password: "
		read ans2
		echo ""
		stty echo

		if [ "$ans" != "$ans2" ]; then
			echo "Passwords do no match, aborting..."
			stty echo
			ext
		fi

		echo "$ans" | sha1sum > "$REPO/passwd"
		echo "$ans" > "$REPO/tmp"
		encrypt
	fi
}

function encrypt
{
	cd "$DMZ"
	for i in $(find -type l); do
		if [ -f "$DOTFILES/$i" ]; then
			rm "$DOTFILES/$i"
		fi
		cp -P --parents "$i" "$DOTFILES"
	done


	for i in $(find -not -type d -and -not -type l); do
		mkdir -p $(dirname "$DOTFILES/$i")
		if [ -f "$DOTFILES/$i" ]; then
			sum=$(sha1sum "$i" | sed 's/\ .*//')
			compare=""
			if [ -f "$DOTFILES/$i.hash" ]; then
				compare=$(cat "$DOTFILES/$i.hash")
			fi
			if [ "$sum" == "$compare" ]; then
				continue;
			fi
			rm "$DOTFILES/$i"
		fi
		if [ -z "$PASSWD" ]; then pprompt "encryption"; fi
		echo "-->Encrypting $(echo $i | cut -c 3-)"
		gpg -c --batch --passphrase-file "$REPO/tmp" -o "$DOTFILES/$i" "$i"
		chmod $(stat -c '%a' "$i") "$DOTFILES/$i"
		sha1sum "$i" | sed 's/\ .*//' > "$DOTFILES/$i.hash"
	done
}

function decrypt
{
	for i in $CRYPTFILES; do
		if echo $i | grep -qv ":"; then i=$(echo "$i:common"); fi

		ownrs=($(echo $i | rev | sed s/\:.*// | sed s/\,/\ /g | rev))
		ownrs=($(for z in ${ownrs[@]}; do echo $z; done | sort))
		filename=$(echo $i | sed s/\:.*//);

		for k in `seq 0 $(expr ${#ownrs[@]} - 1)`; do

			if [ ! -f "$DOTFILES/${ownrs[$k]}/$filename"  ]; then
				echo "--> File ${ownrs[$k]}/$filename does not yet exist in the"\
					"repo. Please run update/encrypt to populate repository"
				continue
			fi

			mkdir -p "$(dirname "$DMZ/${ownrs[$k]}/$filename")"

			copy=0
			if [ -f "$DMZ/${ownrs[$k]}/$filename" ]; then
				if [ -h "$DMZ/${ownrs[$k]}/$filename" ]; then
					copy=1
				else
					sum=$(sha1sum "$DMZ/${ownrs[$k]}/$filename" | \
						sed 's/\ .*//')
					temp="$DOTFILES/${ownrs[$k]}/$filename"
					if [ -h "$temp" ]; then
						temp=$(readlink "$temp")
					fi
					if [ ! -f "$temp" ]; then
						temp=""
					else
						temp=$(cat "$temp.hash")
					fi

					if [ "$sum" != "$temp" ]; then
						echo -e "Your local version of $filename"\
							"(${ownrs[$k]}) differs from the version in the"\
							"repository\n"

						yesno "Do you want to overwrite the local version?"

						if [ $? == 1 ]; then copy=1; fi
					fi
				fi
			else
				copy=1
			fi

			if [ $copy == 1 ]; then
				if [ -h "$DOTFILES/${ownrs[$k]}/$filename" ]; then
					cd "$DOTFILES"
					cp -P --parents "${ownrs[$k]}/$filename" "$DMZ"
					continue
				fi

				if [ -z "$PASSWD" ]; then pprompt "decryption"; fi

				echo "-->Decrypting $filename"
				gpg --quiet --batch --decrypt --passphrase-file "$REPO/tmp" \
					--output "$REPO/mid" "$DOTFILES/${ownrs[$k]}/$filename"
				chmod $(stat -c '%a' "$DOTFILES/${ownrs[$k]}/$filename") \
					"$REPO/mid"

				if [ -f "$DMZ/${ownrs[$k]}/$filename" ]; then
					rm "$DMZ/${ownrs[$k]}/$filename"
				fi

				mv "$REPO/mid" "$DMZ/${ownrs[$k]}/$filename"
			fi
		done
	done
}

function update
{
	if [ -f "$REPO/hard" ]; then hardupdate; return; fi

	echo "Commencing normal files update..."
	symlink "$NORMFILES" "$DOTFILES" "$1"

	echo "Commencing encrypted files update..."
	symlink "$CRYPTFILES" "$DMZ" "$1"

	restore "$1"
	echo "Commencing unencrypted files cleanup..."
	cleanup "$DOTFILES" $NORMFILES $CRYPTFILES
	echo "Commencing encrypted files cleanup..."
	cleanup "$DMZ" $CRYPTFILES

	cd $REPO
	if ! git diff --exit-code "cryptlist" > /dev/null; then
		yesno "The cryptlist has changed since the last commit. Would you like"\
			"to encrypt the changes?"
		if [ $? == 1 ]; then encrypt; fi
	fi
}

function hardupdate
{
	echo "Commencing hard update of normal files..."
	copytorepo "$NORMFILES" "$DOTFILES" "$1"
	echo "Commencing hard update of encrypted files..."
	copytorepo "$CRYPTFILES" "$DMZ" "$1"
	echo "Commencing unencrypted files cleanup..."
	cleanup "$DOTFILES" $NORMFILES $CRYPTFILES
	echo "Commencing encrypted files cleanup..."
	cleanup "$DMZ" $CRYPTFILES

	cd "$REPO"
	if ! git diff --exit-code "$REPO/cryptlist" > /dev/null; then
		if ! yesno "The cryptlist has changed since the last commit. Would you"\
			"like to encrypt the changes?"; then
			encrypt "$1"
		fi
	fi
}

function copytorepo
{
	FILELIST=$1
	CDFILES=$2

	cd $HOME
	owner=$3

	if [ -z "$owner" ]; then
		for i in $(echo "$FILELIST" | grep -v "\:"); do
			mkdir -p "$CDFILES/common"
			pstatus $i "common" "Copying"
			if [ ! "$HOME/$i" -ef "$CDFILES/common/$i" ]; then
				cp -L --parents "$i" "$CDFILES/common"
			fi
		done;
		owner=$HOSTNAME
	fi

	for i in $(echo "$FILELIST" | grep "$owner"); do
		ownrs=($(echo $i | rev | sed s/\:.*// | sed s/\,/\\n/g | rev))
		filename=$(echo $i | sed s/\:.*//)

		for k in "${ownrs[@]}"; do
			if [ ! -d "$CDFILES/$k" ]; then mkdir "$CDFILES/$k"; fi

			pstatus "$filename" "$k" "Copying"
			if [ -h "$CDFILES/$k/$filename" ]; then
				rm "$CDFILES/$k/$filename"
			fi
			if [ ! "$HOME/$filename" -ef "$CDFILES/$k/$filename" ]; then
				cp -L --parents "$filename" "$CDFILES/$k"
			fi
		done
	done
}

function symlink
{
	FILELIST=$1
	CDFILES=$2

	cd $HOME;
	owner=$3

	if [ -z "$owner" ]; then
		for i in $(echo "$FILELIST" | grep -v "\:"); do
			if [ ! -f "$CDFILES/common/$i" ]; then
				mkdir -p "$CDFILES/common"
				pstatus $i "common"
				cp -L --parents "$i" "$CDFILES/common"
				rm "$i"
			fi
		done;
		owner=$HOSTNAME
	fi

	for i in $(echo "$FILELIST" | grep "$owner"); do
		ownrs=($(echo $i | rev | sed s/\:.*// | sed s/\,/\ /g | rev))
		filename=$(echo $i | sed s/\:.*//)
		ownrs=($(for z in ${ownrs[@]}; do echo $z; done | sort))

		splits=$(find "$CDFILES" -lname "*${ownrs[0]}/$filename")
		for k in $(seq 0 `expr ${#ownrs[@]} - 1`); do
			splits=$(echo "$splits" | grep -v "${ownrs[$k]}")
		done

		if [ -n "$splits" ] && [ -f "$CDFILES/${ownrs[0]}/$filename" ]
		then
			for k in $splits; do
				temp="$CDFILES/"
				z=$(echo $k | cut -c $(expr ${#temp} + 1)- | sed "s/\/.*//g")
				pstatus "$filename" "$z" "Splitting"

				rm $k
				cp "$CDFILES/${ownrs[0]}/$filename" $k
			done
		fi

		for k in $(seq 0 `expr ${#ownrs[@]} - 1`); do

			if [ ! -d "$CDFILES/${ownrs[$k]}" ]; then
				mkdir -p "$CDFILES/${ownrs[$k]}"; fi

			if [ ! -f "$CDFILES/${ownrs[$k]}/$filename" ]; then
				if [ $k == "0" ]; then
					pstatus "$filename" "${ownrs[0]}"
					cp -L --parents "$filename" "$CDFILES/${ownrs[0]}"

					rm "$HOME/$filename"
				else
					pstatus "(${ownrs[0]})  $filename" "${ownrs[$k]}" "Linking"
					mkdir -p "$(dirname "$CDFILES/${ownrs[$k]}/$filename")"
					ln -rs "$CDFILES/${ownrs[0]}/$filename" \
					"$CDFILES/${ownrs[$k]}/$filename"
				fi
			else
				if [ "$k" == "0" ] && \
					[ -h "$CDFILES/${ownrs[$k]}/$filename" ]; then
					pstatus "$filename" "${ownrs[0]}"
					rm "$CDFILES/${ownrs[$k]}/$filename"
					cp -L --parents "$filename" "$CDFILES/${ownrs[$k]}"
				fi

				if [ "$k" != "0" ] && \
					[ ! -h "$CDFILES/${ownrs[$k]}/$filename" ]; then

					if diff "$CDFILES/${ownrs[0]}/$filename" \
						"$CDFILES/${ownrs[$k]}/$filename" > /dev/null;then
						rm "$CDFILES/${ownrs[$k]}/$filename"
						ln -rs "$CDFILES/${ownrs[0]}/$filename" \
							"$CDFILES/${ownrs[$k]}/$filename"
						continue
					fi

					pstatus "$filename" "varies" "Merging"
					echo "Different versions of the same file are now being" \
					"linked together. Which version do you want to use?"

					mergers=()
					for z in $(seq 0 `expr ${#ownrs[@]} - 1`); do
						if [ -f "$CDFILES/${ownrs[$z]}/$filename" ]; then
							mergers=(${mergers[@]} ${ownrs[$z]})
						fi
					done

					for z in $(seq 0 `expr ${#mergers[@]} - 1`); do
						echo "$(expr $z + 1)) ${mergers[$z]}"
					done

					ans=""
					while true; do
						echo -ne "\nYour answer (1-${#mergers[@]}): "
						read ans

						if ! [[ $ans =~ ^[0-9]+$ ]]; then
							echo "Please enter a number"
							continue
						fi

						if [ $ans -ge 1 ] && [ $ans -le ${#mergers[@]} ]; then
							break
						else
							echo "Invalid option, please enter a number "\
								"between 1 and ${#mergers[@]}"
						fi
					done
					ans=`expr $ans - 1`

					if [ $ans -ne 0 ]; then
						rm "$CDFILES/${ownrs[0]}/$filename"
						cp "$CDFILES/${ownrs[$ans]}/$filename" \
							"$CDFILES/${ownrs[0]}/$filename"
					fi

					for z in $(seq 1 `expr ${#ownrs[@]} - 1`); do
						rm "$CDFILES/${ownrs[$z]}/$filename"
					done

					pstatus "(${ownrs[0]}) $filename" "${ownrs[$k]}" "Linking"
					if [ -f "$CDFILES/${ownrs[$k]}/$filename" ]; then
						rm "$CDFILES/${ownrs[$k]}/$filename"
					fi
					ln -rs "$CDFILES/${ownrs[0]}/$filename" \
					"$CDFILES/${ownrs[$k]}/$filename"
				fi

				if [ "$k" != "0" ] && \
					[ -h "$CDFILES/${ownrs[$k]}/$filename" ]; then
					rm "$CDFILES/${ownrs[$k]}/$filename"
					ln -rs "$CDFILES/${ownrs[0]}/$filename" \
					"$CDFILES/${ownrs[$k]}/$filename"
				fi
			fi
		done;
	done;
}

function yesno
{
	echo -n $* "[Y/n]: "
	read ans

	if [ "$ans" == "Y" ] || [ "$ans" == "y" ] || [ -z "$ans" ]; then
		return 1
	else
		return 0
	fi
}

function lnconf
{
	if [ -h "$2" ]; then
		rm "$2"
	fi

	if [ -f "$2" ] && [ ! -h "$2" ]; then
		yesno "File $3 already exists in home directory. Do you want to"\
			"overwrite it?"

		if [ "$?" == 1 ]; then
			rm "$2"
		else
			return
		fi
	fi
	ln -s "$1" "$2"
}

function restore
{
	if [ -f "$REPO/hard" ]; then hardrestore; return; fi

	cleanhome
	echo "Commencing unencrypted repo linking..."
	homelink "$NORMFILES" "$DOTFILES" "$1"
	echo "Commencing encrypted repo linking..."
	homelink "$CRYPTFILES" "$DMZ" "$1"
}

function homelink
{
	FILELIST=$1
	CDFILES=$2

	cd "$CDFILES"
	owner=$3

	if [ -z "$owner" ]; then
		for i in $(echo "$FILELIST" | grep -v "\:"); do
			if [ "$(dirname "$i")" != "." ]; then
				mkdir -p "$(dirname "$HOME/$i")"
			fi

			if [ ! -f "$CDFILES/common/$i" ]; then
				echo "-->Can't link $i (its either not yet decrypted or it has"\
					"not been copied to the repository yet)"
				continue
			fi

			lnconf "$CDFILES/common/$i" "$HOME/$i" "$i"
		done
		owner=$HOSTNAME
	fi

	for i in $(echo "$FILELIST" | grep "$owner"); do
		ownrs=($(echo $i | rev | sed s/\:.*// | sed s/\,/\ /g | rev))
		ownrs=($(for z in ${ownrs[@]}; do echo $z; done | sort))
		filename=$(echo $i | sed s/\:.*//);

		if [ ! -f "$CDFILES/${ownrs[0]}/$filename" ]; then
			echo "-->Can't link $filename (its either not yet decrypted or it"\
				"has not been copied to the repository yet)"
			continue
		fi

		if [ "$(dirname "$filename")" != "." ]; then
			mkdir -p "$(dirname "$HOME/$filename")"
		fi

		lnconf "$CDFILES/${ownrs[0]}/$filename" "$HOME/$filename" \
		"$filename"
	done
}

function generate
{
	encrypt
	cd "$REPO"
	git add --all
	OLDIFS=$IFS
	IFS=$(echo -en '\n')
	message=$(git status --porcelain | grep "dotfiles" | grep -v '.hash' | \
		tr '\n' ';')
	IFS=$OLDIFS

	message=$(echo $message |  sed 's/;/;\ /g')

	message=$(echo $message | \
		sed 's/dotfiles\///g' | \
		sed 's/A/added/g' | \
		sed 's/R/renamed/g' | \
		sed 's/M/modified/g' | \
		sed 's/D/deleted/g' | \
		sed 's/C/copied/g' | \
		sed 's/T/typechanged/g')

	if [ -z "$message" ]; then
		echo "No changes to repository..."
		return
	fi

	git commit -m "Changes: $(echo "$message" | rev | cut -c 2- | rev)"

	if [ -n "$(git remote -v)" ]; then
		yesno "Remote detected, do you want to push (sync) to it?"
		if [ "$?" == 1 ]; then
			git push
		fi
	fi
}

function cleanup
{
	CDFILES=$1
	FILELIST=${@:2}

	if [ -z "$(ls -A $CDFILES)" ]; then
		return
	fi

	cd "$CDFILES"
	for i in *; do
		echo "Cleanup - entering $i..."
		cd "$i"

		for k in $(find -not -type d); do
			if [ $k == "." ]; then
				continue;
			fi
			k=$(echo $k | cut -c 3-);

			z=""
			if [ "$i" != "common" ]; then
				z="$i"
			fi

			if [[ $k =~ .hash$ ]]; then
				temp=$(echo $k | sed 's/\.hash//')
				l=$(echo "$FILELIST" | tr ' ' '\n' | grep "$temp" | grep "$z")

				if [ -n "$l" ]; then
					ownrs=($(echo $l| rev | sed 's/\:.*//' | sed 's/\,/\ /g' | \
						rev))
					ownrs=($(for p in ${ownrs[@]}; do echo $p; done | sort))
					if [ "${ownrs[0]}" == "$z" ]; then
						k=$temp
					fi
				fi
			fi

			if [ -n "$z" ]; then
				if [ -z "$(echo "$FILELIST" | tr ' ' '\n' | grep "$k" | grep \
					"[:,\,]$z\,\|[:,\,]$z\$" )" ]; then
					pstatus "$i/$k" "$i" "Removing"
					rm "$k"
				fi;
			else
				if ! echo "$FILELIST" | tr ' ' '\n' | grep "$k" | grep -qv ":";
				then
					pstatus "$i/$k" "$i" "Removing"
					rm "$k"
				fi
			fi
		done;
		cd "$CDFILES"
	done;

	find "$CDFILES" -not -name "$(basename $CDFILES)" -and -empty -and -type d \
	-delete
}

function cleanhome
{
	echo "Cleaning up old repo links..."
	for i in $(find $HOME -type l -not -wholename "$REPO/*"); do
		if [[ `readlink $i` =~ $REPO ]]; then rm $i; fi
	done
}

function hardrestore
{
	echo "Commencing hard restore of normal files..."
	copytohome "$NORMFILES" "$DOTFILES"
	echo "Commencing hard restore of encrypted files..."
	copytohome "$CRYPTFILES" "$DMZ"
}

function copytohome
{
	FILELIST=$1
	CDFILES=$2
	category=$3

	cd "$CDFILES"

	if [ -z "$category" ]; then
		cd common
		for i in $(find . -not -type d); do
			i="$(echo $i | cut -c 3-)"
			pstatus "$i" "common" "Copying"
			if [ -f "$HOME/$i" ]; then
				rm "$HOME/$i"
			fi
			cp --parents "$i" "$HOME"
		done
		cd ..

		if [ -d "$HOSTNAME" ]; then
			cd "$HOSTNAME"
		else
			echo "Folder for $HOSTNAME not found..."
			return
		fi

		for i in $(find . -not -type d); do
			i="$(echo $i | cut -c 3-)"
			pstatus "$i" "$HOSTNAME" "Copying"
			if [ -f "$HOME/$i" ]; then
				rm "$HOME/$i"
			fi
			cp -L --parents "$i" "$HOME"
		done
	else
		if [ -d "$category" ]; then
			cd "$category"
		else
			echo "Category $category not found..."
		fi

		for i in $(find . -not -type d); do
			i="$(echo $i | cut -c 3-)"
			pstatus "$i" "$category" "Copying"
			if [ -f "$HOME/$i" ]; then
				rm "$HOME/$i"
			fi
			cp -L --parents "$i" "$HOME"
		done
	fi

	echo "Finished copying..."
}

function init
{
	echo "Initializing dotgit repo..."
	if [ ! -d "$REPO/.git" ]; then git init; fi
	touch filelist
	touch cryptlist

	ignore=0
	if [ -f "$REPO/.gitignore" ]; then
		if ! grep -q "dmz" "$REPO/.gitignore"; then
			ignore=1
		fi
	else
		ignore=1
	fi

	if [ $ignore -eq 1 ]; then
		echo "dmz" >> .gitignore
		echo "tmp" >> .gitignore
		echo "mid" >> .gitignore
	fi

	create=0
	if [ -f "$REPO/.git/hooks/post-merge" ]; then
		if ! grep -q "dotgit decrypt" "$REPO/.git/hooks/post-merge"; then
			create=1
		fi
	else
		create=1
	fi

	if [ $create -eq 1 ]; then
		echo "Creating encryption hooks..."
		echo "exec < /dev/tty" >> .git/hooks/post-merge
		echo "dotgit decrypt" >> .git/hooks/post-merge
		chmod +x .git/hooks/post-merge
	fi

	echo "Initialized dotgit repo in $PWD"
}

function pdiff
{
	cd "$REPO"
	git add --all
	OLDIFS=$IFS
	IFS=$(echo -en '\n')
	message=$(git status --porcelain | grep "dotfiles" | grep -v '.hash')

	message=$(echo $message | \
		sed 's/dotfiles\///g' | \
		sed 's/A/Added/g' | \
		sed 's/R/Renamed/g' | \
		sed 's/M/Modified/g' | \
		sed 's/D/Deleted/g' | \
		sed 's/C/Copied/g' | \
		sed 's/T/Typechange/g')

	if [ -z "$message" ]; then
		echo "No changes to dotfiles folder..."
	else
		echo "$message"
	fi
	IFS=$OLDIFS

	message=""
	for i in $(find "$DMZ" -not -type l -and -not -type d); do
		i=$(echo $i | cut -c `expr ${#DMZ} + 2`-)
		if [ -f "$DOTFILES/$i.hash" ]; then
			sum=$(sha1sum "$DMZ/$i" | sed 's/\ .*//')
			comp=$(cat "$DOTFILES/$i.hash")
			if [ $comp != $sum ]; then
				message=$(echo -e "$message" "\nModified $i")
			fi
		else
			message=$(echo -e "$message" "\nAdded $i")
		fi
	done

	if [ -n "$message" ]; then
		echo -e "\nUnencrypted changes (does not show removed files):"\
			"$message\n"
	fi

	git reset -q
}

function ext
{
	if [ -f "$REPO/tmp" ]; then
		rm "$REPO/tmp"
	fi
	stty sane

	if [ -z "$1" ]; then
		exit 1
	else
		exit $1
	fi
}

if [[ $# -eq 0 ]]; then
	phelp;
	exit;
fi;

safeguards $1
if [[ $1 != "init" ]]; then cfilelist; fi

trap ext SIGINT

case "$1" in
	"update")update "$2";;
	"restore")restore "$2";;
	"generate")generate;;
	"hard-restore")hardrestore "$2";;
	"init")init;;
	"encrypt")encrypt;;
	"decrypt")decrypt;;
	"clean")cleanhome;;
	"passwd")passwd;;
	"diff")pdiff;;
	"help")phelp;;
	*)echo -e "$1 is not a valid argument."; exit 1;;
esac;

ext 0
