$count = "advsearch/your_agent/othello_minimax_count.py"

$mask = "advsearch/your_agent/othello_minimax_mask.py"

$custom = "advsearch/nah_id_lose/othello_minimax_custom.py"

$custom_old = "advsearch/your_agent/othello_minimax_custom.py"

$human = "advsearch/humanplayer/agent.py"

$random = "advsearch/randomplayer/agent.py"


$agent  = $custom

$opponent = $custom


$time_seconds = 5

$step_seconds = 0.001

python server.py othello $agent $opponent -d $time_seconds -p $step_seconds

# python server.py othello $opponent $agent -d $time_seconds -p $step_seconds

