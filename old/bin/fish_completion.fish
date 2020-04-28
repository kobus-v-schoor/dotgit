# completion for https://github.com/kobus-v-schoor/dotgit

function __fish_dotgit_no_subcommand -d 'Test if dotgit has yet to be given the subcommand'
	for i in (commandline -opc)
		if contains -- $i init upgrade restore clean encrypt decrypt passwd diff generate help
			return 1
		end
	end
	return 0
end

complete -f -n '__fish_dotgit_no_subcommand' -c dotgit -a 'init' -d 'Setup a new dotgit repository'
complete -f -n '__fish_dotgit_no_subcommand' -c dotgit -a 'update' -d 'Update the repository structure to match filelists'
complete -f -n '__fish_dotgit_no_subcommand' -c dotgit -a 'restore' -d 'Create links from the home folder to the repository'
complete -f -n '__fish_dotgit_no_subcommand' -c dotgit -a 'clean' -d 'Remove links in the home folder'
complete -f -n '__fish_dotgit_no_subcommand' -c dotgit -a 'encrypt' -d 'Encrypt all files'
complete -f -n '__fish_dotgit_no_subcommand' -c dotgit -a 'decrypt' -d 'Decrypt all files'
complete -f -n '__fish_dotgit_no_subcommand' -c dotgit -a 'passwd' -d 'Change the dotgit password'
complete -f -n '__fish_dotgit_no_subcommand' -c dotgit -a 'diff' -d 'Print the current changes'
complete -f -n '__fish_dotgit_no_subcommand' -c dotgit -a 'generate' -d 'Generate and push the changes'
complete -f -n '__fish_dotgit_no_subcommand' -c dotgit -a 'help' -d 'Display the help'
