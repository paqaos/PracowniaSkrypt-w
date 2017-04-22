#!/bin/bash

#kolkokrzyzyk

ilosc=9
i=1
tab=("1" "2" "3" "4" "5" "6" "7" "8" "9")

row=1
col=1
gracz=1
tura=1
play=true
pole=0
process=true
znak="x"

while $play ; do

	for row in {1..3}
	do
		echo "${tab[$[$row-1]*3]}""${tab[$[$row-1]*3+1]}""${tab[$[$row-1]*3+2]}"
	done

	pole=0	
	if [ "$gracz" -eq 1 ] ; then
		echo 'tura gracza x: ' $tura
		znak="x"
	else
		echo 'tura gracza o: ' $tura
		znak="o"
	fi
	echo $znak

	while $process ; do
		read pole
		if [ "$pole" -le 9 ] && [ "$pole" -ge 1 ]; then
			poleVal=$[tab[$[$pole-1]]]
			if [ "$poleVal" -eq $pole ]; then
				process=false
				id=$[$pole-1]
				if [ "$gracz" -eq 1 ] ; then
					tab[$id]="x"
				else
					tab[$id]="o"
				fi
				echo $[tab[$[$pole-1]]]
				echo 'brawo'
			else
				echo 'pole zajete'
			fi
		fi 
	done
	process=true
	
	row=$[$[$pole-1]/3]
	col=$[$[$pole-1]%3]
	el=$[$[$row]*3]

	firstrow="${tab[$[$el+0]]}"
	secondrow="${tab[$[$el+1]]}"
	thirdrow="${tab[$[$el+2]]}"

	firstcol="${tab[$[$col]]}"
	secondcol="${tab[$[$col+3]]}"
	thirdcol="${tab[$[$col+6]]}"
	
	if [ "$secondrow" == $thirdrow ] && [ "$secondrow" == $firstrow ] ; then
		echo "koniec wygrana " ${secondrow}
		play=false
	fi

	if [ "$secondcol" == $thirdcol ] && [ "$secondcol" == $firstcol ] ; then
		echo "koniec wygrana " ${secondcol}
		play=false
	fi

	echo "${tab[0]}"
	if [ "${tab[0]}" == $tab[4] ] && [ "${tab[0]}" == $tab[8] ] ; then
		echo "koniec wygrana " $tab[4]
		play=false
	fi

	echo $row $col

	tura=$[$tura+1]
	if [ "$gracz" -eq 1 ] ; then
		gracz=2
	else
		gracz=1
	fi

	if [ "$tura" -eq 10 ] ; then
		play=false
		echo "remis"
	fi
done

