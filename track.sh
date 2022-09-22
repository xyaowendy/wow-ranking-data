dungeo="tianjie hongtu kashang kaxia lajichang chejian matou chezhan"
realm="fenghuang ge ranshao siwang yiseng ansu xuese"
realm="$realm kesjd bfg edsl blkd yzas wjzh pjzd gwzg"
realm="$realm baiyin luoning zhuzhai xiongmao jinse"
# periodId="865 864 863 862 861 860 859 858 857"
periodId="872"
 dungeo="tianjie"
 realm="fenghuang"

function track(){
    dir=./log.$periodId
    for d in $dungeo;do
        mkdir -p $dir
        for r in $realm;do
            for p in $periodId;do
                for page in `seq 1 1`;do
                    echo "tracking dungeo:$d realm:$r periodId:$p page: $page ..."
                    python3 track.py $d $r $p $page > $dir/dungeo_$d.realm_$r.$p.page$page.log
                    echo "tracking dungeo:$d realm:$r periodId:$p page: $page done"
                done
            done
        done
    done
}

track
