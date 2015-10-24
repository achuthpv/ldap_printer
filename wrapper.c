/**
 * Wrapper for account.py to be run as root.
 * This is to keep all the data in account.txt
 *
**/

#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>

int main(int aArgNum, char **aArgs){
	int scriptReturn;
	char *uname = getlogin();
	char buffer[256];
	setuid(0);	//become root
	sprintf(buffer,"/usr/bin/python /home/achuth/scripts/account.py %s",uname);
	scriptReturn = system(buffer);
	return scriptReturn%10;
}
