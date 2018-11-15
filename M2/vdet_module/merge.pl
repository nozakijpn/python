#!/usr/bin/perl


$interval = 0.25; # [sec]

&readData;

sub readData {
    local($count) = 0;
    local($file);
    local(@tmp);
    local($i) = 0;

    local($old_kind) = 0;

    $file = $ARGV[0];
    open(FILE, $file) || warn "Can't open file; $file\n";
   
    while (<FILE>)
    {
	@tmp = split(/\s+/);

	$time[$count] = $tmp[0];
	$flag[$count] = $tmp[1];
#	$kind[$count] = $tmp[2]-1;
	$kind[$count] = $tmp[2];

	$count ++;
    }


    for($i = 0; $i < $count; $i++)
    {
	if ($old_kind == $kind[$i]) # “¯‚¶‚à‚Ì‚ð‚­‚Á‚Â‚¯‚é
	{
	    $flag[$i] = 1;  # NOP
	}

	if ($time[$i+1] - $time[$i] < $interval) # ŽŸ‚ÌƒtƒŒ[ƒ€‚Æ‚ÌŠÔŠu‚ª¬‚³‚¢
	{
	    if ($kind[$i+1] != $kind[$i]) # ’Z‚¢‚à‚Ìœ‹Ž‚·‚é
	    {
		$flag[$i] = 1;  # NOP		
	    }
	}

	$old_kind = $kind[$i];
    }

    for($i = 0; $i < $count; $i++)
    {
	if($flag[$i] == -1)
	{
	    $tmp_time  = $time[$i];
	    for($j = $i+1; $j < $count; $j++)
	    {
		# printf("->$time[$i]\t$flag[$i]\t$kind[$i]\n");
		if($flag[$j] == -1)
		{
		    # printf("=>$time[$j]\t$flag[$j]\t$kind[$j]\n");
		    if ($time[$j] - $tmp_time < $interval)
		    {
			$flag[$i] = 2;  
			last;
		    }
		    else 
		    {
			last;
		    }
		}
	    }
	}
    }


    for($i = 0; $i < $count; $i++)
    {
	if($flag[$i] == -1)
	{
	    for($j = $i+1; $j < $count; $j++)
	    {
		if(($flag[$j] == -1) && ($kind[$j] == $kind[$i]))
		{
		    $flag[$j] = 3;  
		}
		if(($flag[$j] == -1) && ($kind[$j] != $kind[$i])) 
		{
		    last;
		}
	    }
	}
    }



#    $lbl = $kind[0];
#    for($i = 0; $i < $count; $i++)
#    {
#	if($flag[$i] == -1) 
#	{
#	    printf("$time[$i]\t$flag[$i]\t$kind[$i]\n");
#	}
#	if($flag[$i] == -1)
#	{
#	    $lbl = $kind[$i];
#	}
#	print "$lbl\n";
#    }


    # $begin = $time[0]; 
    $begin = 0.046; 
    $lbl   = $kind[0];

    for($i = 0; $i < $count; $i++)
    {
	if (($flag[$i] != -1) && ($i != $count-1))
	{
	    next;
	}

	$num = int(($time[$i] - $begin) / 0.023219955+0.5);
	# print "! ", $num, "\n";
	
	for($j = 0; $j < $num; $j++)
	{
	    # print $begin + 0.023219955*($j), " ", $lbl, "\n";
	    print $lbl, "\n";
	}
	$begin = $time[$i];
	$lbl = $kind[$i];
    }
    
}
