dir=$(dirname $0)
site=$(basename $0)
${dir}/deploy $@ $site 
