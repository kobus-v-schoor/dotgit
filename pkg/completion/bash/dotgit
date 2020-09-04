#! /bin/bash

function _dotgit {
	local has_action=0

	# iterate through the current args to check if we are trying to complete an
	# action or a category
	for word in "${COMP_WORDS[@]}"; do
		# skip current word
		[[ $word == ${COMP_WORDS[COMP_CWORD]} ]] && continue

		# skip the actual dotgit command
		[[ $word == "dotgit" ]] && continue

		# check if the cmd flag starts with a dash to check if it is a flag or
		# an action
		if [[ ${word} != -* ]]; then
			has_action=1
			break
		fi
	done

	# no action so complete for action name
	if [[ $has_action -eq 0 ]]; then
		COMPREPLY+=("init")
		COMPREPLY+=("update")
		COMPREPLY+=("restore")
		COMPREPLY+=("clean")
		COMPREPLY+=("diff")
		COMPREPLY+=("commit")
	else
		# there is alreay an action specified, so parse the filelist for
		# category names
		COMPREPLY+=("common")
		COMPREPLY+=("$HOSTNAME")

		if [[ -f filelist ]]; then
			while read line; do
				# remove leading whitespace characters
				line="${line#"${line%%[![:space:]]*}"}"
				# remove trailing whitespace characters
				line="${line%"${line##*[![:space:]]}"}"

				# skip empty lines
				[[ -z $line ]] && continue

				# skip comment lines
				[[ $line =~ \# ]] && continue

				# check if it is a category group, if not parse categories
				if [[ $line =~ = ]]; then
					# remove all categories in category group
					COMPREPLY+=(${line%%=*})
				elif [[ $line =~ : ]]; then
					# remove filename
					line=${line##*:}
					# split into categories
					IFS=',' read -ra categories <<< "$line"
					# add categories to completion list
					COMPREPLY+=("${categories[@]}")
				fi
			done < filelist
		fi
	fi

	# add other command-line flags
	COMPREPLY+=("-h" "--help")
	COMPREPLY+=("-v" "--verbose")
	COMPREPLY+=("--dry-run")
	COMPREPLY+=("--hard")

	# filter options that start with the current word
	COMPREPLY=($(compgen -W "${COMPREPLY[*]}" -- ${COMP_WORDS[COMP_CWORD]}))
}

complete -F _dotgit dotgit
