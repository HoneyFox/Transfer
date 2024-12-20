AGM_84D =
{
	category		= CAT_MISSILES,
	name			= "AGM_84D",
	user_name		= _("AGM-84D"),
	scheme			= "anti_ship_missile_prog_path_stpos_ctrl",
	class_name		= "wAmmunitionAntiShip",
	model			= "agm-84d",
	mass			= 540,
	
	wsTypeOfWeapon 	= {wsType_Weapon,wsType_Missile,wsType_AS_Missile,WSTYPE_PLACEHOLDER},

	Escort			= 0,
	Head_Type		= 5,
	sigma			= {20, 20, 20},
	M				= 540.0,
	H_max			= 10000.0,
	H_min			= -1,
	Diam			= 343.0,
	Cx_pil			= 8,
	D_max			= 190000.0,
	D_min			= 5000.0,
	Head_Form		= 0,
	Life_Time		= 100000,
	Nr_max			= 6,
	v_min			= 170.0,
	v_mid			= 237.5,
	Mach_max		= 0.95,
	t_b				= 0.0,
	t_acc			= 5.0,
	t_marsh			= 10000.0,
	Range_max		= 190000.0,
	H_min_t			= 500.0,
	Fi_start		= 0.35,
	Fi_rak			= 3.14152,
	Fi_excort		= 0.7,
	Fi_search		= 99.9,
	OmViz_max		= 99.9,
	X_back			= 0,
	Y_back			= 0,
	Z_back			= 0,
	Reflection		= 0.1691,
	KillDistance	= 0.0,
	
	manualWeaponFlag = 2,
	
	LaunchDistData = 
	{	
		14,		8,
		
					50,		75,		100,	125,	150,	200,	250,	300,	
				
		100,		0,		0,		0,		132000,	136000,	141000,	145000,	148000,	
		200,		0,		0,		0,		133000,	137000,	142000,	145000,	148000,	
		300,		0,		0,		129000,	135000,	138000,	142000,	146000,	149000,	
		500,		0,		0,		133000,	136000,	139000,	143000,	146000,	149000,	
		600,		0,		128000,	134000,	137000,	139000,	143000,	147000,	149000,	
		800,		0,		131000,	135000,	138000,	140000,	144000,	147000,	149000,	
		900,		126000,	132000,	135000,	138000,	140000,	144000,	148000,	149000,	
		1000,		128000,	133000,	136000,	137000,	140000,	144000,	148000,	151000,	
		2000,		133000,	136000,	138000,	141000,	143000,	147000,	151000,	154000,	
		4000,		137000,	140000,	143000,	146000,	149000,	153000,	156000,	160000,	
		6000,		142000,	144000,	147000,	150000,	153000,	158000,	161000,	165000,	
		8000,		145000,	148000,	151000,	154000,	157000,	162000,	167000,	171000,	
		10000,		148000,	151000,	155000,	158000,	161000,	168000,	174000,	178000,	
		12000,		152000,	156000,	160000,	164000,	168000,	177000,	185000,	191000,	
	},
	
	MinLaunchDistData = 
	{
		10, 6,
					50,		100,	150,	200,	250,	300,
				
		3000,		5000,	5000,	6000,	6000,	7000,	7000,	
		4000,		5000,	6000,	7000,	8000,	8000,	9000,	
		5000,		5000,	7000,	18000,	19000,	20000,	20000,	
		6000,		5000,	27000,	29000,	31000,	32000,	33000,	
		7000,		5000,	38000,	41000,	43000,	44000,	45000,	
		8000,		47000,	50000,	53000,	56000,	57000,	59000,	
		9000,		60000,	63000,	66000,	69000,	71000,	73000,	
		10000,		73000,	76000,	80000,	83000,	85000,	87000,	
		11000,		86000,	90000,	94000,	98000,	101000,	103000,	
		12000,		100000,	105000,	109000,	113000,	116000,	119000,	
	},
	
	add_attributes = {"Cruise missiles"},
	
	shape_table_data =
	{
		{
			name		= "AGM-84D",
			file		= "agm-84d",
			life		= 1,
			fire		= { 0, 1},
			username	= _("AGM-84D"),
			index		= WSTYPE_PLACEHOLDER,
		},
	},
	
	fm = {
		mass        = 540.0,  
		caliber     = 0.343,  
		cx_coeff    = {1,0.39,0.38,0.236,1.31},
		L           = 3.85,
		I           = 1 / 12 * 661.5 * 3.85 * 3.85,
		Ma          = 0.68,
		Mw          = 1.116,
		wind_sigma	= 0.0,
		wind_time	= 1000.0,
		Sw			= 0.7,
		dCydA		= {0.07, 0.036},
		A			= 0.5,
		maxAoa		= 0.3,
		finsTau		= 0.05,
		Ma_x		= 3,
		Ma_z		= 3,
		Kw_x		= 0.05,
	},
	
	seeker = {
		delay						= 0.0,
		op_time						= 9999.0,
		FOV							= math.rad(60),
		max_w_LOS					= 0.06,
		max_target_speed			= 33.0,
		max_target_speed_rnd_coeff	= 10.0,
		ship_track_by_default		= 1,
		flag_dist					= 5000.0,
		sens_near_dist				= 10.0,
		sens_far_dist				= 35000.0, --15000.0
		primary_target_filter		= 1,
		add_y						= 3.0,		
	},
	
	autopilot =
	{
		delay						= 1.0,
		Kpv							= 0.046, --0.026
		Kdv							= 12.0, --2.4
		Kiv							= 0.000006,
		Kph							= 40.0, --28.0
		Kdh							= 5.0, --3.0
		Kih							= 0.0,
		cmd_K						= 12.0,
		cmd_Kd						= 10.0,
		glide_height				= 15.0,
		use_current_height			= 1,
		max_vert_speed 				= 160.0, --70.0
		altim_vel_k					= 2.0, --1.0
		finsLimit					= 0.68,
		inertial_km_error			= 0.2,
		max_heading_err_val 		= 0.05, --0.09
		skim_glide_height			= 5.0, --8.0
		pre_maneuver_glide_height	= 15.0, --20.0
		vel_proj_div				= 20.0,
	},
	
	final_autopilot =		
		{
		delay				= 0,
		K					= 60,
		Ki					= 0,
		Kg					= 16,
		finsLimit			= 0.9,		
		useJumpByDefault	= 0,
		J_Power_K			= 2.0,
		J_Diff_K			= 0.8,
		J_Int_K				= 0,
		J_Angle_K			= 0.24,
		J_FinAngle_K		= 0.32,
		J_Angle_W			= 2.4,
		bang_bang			= 0,
		J_Trigger_Vert		= 1,
		loft_add_val		= 1,
	},
	
	triggers_control = {
		action_wait_timer				= 5,	-- wait for dist functions n sen, then set default values
		default_sensor_tg_dist			= 8000, -- turn on seeker and start horiz. correction if target is locked
		default_final_maneuver_tg_dist	= 1000, --4000
		default_straight_nav_tg_dist	= 1000,
		default_destruct_tg_dist		= 1000,	-- if seeker still can not find a target explode warhead after reaching pred. target point + n. km
		trigger_by_path					= 1,
		pre_maneuver_glide_height		= 15,	-- triggers st nav instead of fin. maneuver if h>2*pre_maneuver_glide_height at fin. maneuver distance
	},
	
	controller = {
		boost_start	= 0.001,
		march_start = 0.01,
	},
	
	boost = {				--	air launch - no booster
		impulse								= 0,
		fuel_mass							= 0,
		work_time							= 0,
		boost_time							= 0,
		boost_factor						= 0,
		nozzle_position						= {{0, 0, 0}},
		nozzle_orientationXYZ				= {{0, 0, 0}},
		tail_width							= 0.0,
		smoke_color							= {0.0, 0.0, 0.0},
		smoke_transparency					= 0.0,
		custom_smoke_dissipation_factor		= 0.0,				
	},
	
	march = {
		impulse			= 690,
		fuel_mass		= 138.5,
		work_time		= 9999,
		min_fuel_rate	= 0.005,
		min_thrust		= -100,
		max_thrust		= 3000,
		thrust_Tau		= 0.0017,
		
		nozzle_position						= {{-1.70, 0.0, 0.0}},
		nozzle_orientationXYZ				= {{0.0, 0.0, 0.0}},
		tail_width							= 0.5,
		smoke_color							= {0.0, 0.0, 0.0},
		smoke_transparency					= 0.2,
		custom_smoke_dissipation_factor		= 0.2,	
		
		start_burn_effect			= 1,
		start_effect_delay			= {0.0,		0.3, 	0.8},
		start_effect_time			= {0.7,		1.0, 	0.1},
		start_effect_size			= {0.09,	0.104,	0.11},
		start_effect_smoke			= {0.01,	0.4, 	0.01},
		start_effect_x_pow			= {1.0,		1.0,	1.0},
		start_effect_x_dist			= {1.1,		0.9,	0.0},
		start_effect_x_shift		= {0.15,	0.15,	0.2},
	},
	
	engine_control = {
		default_speed	= 237,
		K				= 265,
		Kd				= 0.01,
		Ki				= 0.001,
	},
	
	warhead		= predefined_warhead("AGM_84A"),
	warhead_air = predefined_warhead("AGM_84A"),
}

declare_weapon(AGM_84D)

declare_loadout({
	category 		= CAT_MISSILES,
	CLSID	 		= "{AGM_84D}",
	attribute		= AGM_84D.wsTypeOfWeapon,
	Count 			= 1,
	Cx_pil			= 0.0018,
	Picture			= "agm84a.png",
	displayName		= AGM_84D.user_name,
	Weight			= AGM_84D.mass,
	Elements  		= {{ShapeName = "agm-84d"}},
})

AGM_84H =
{
	category		= CAT_MISSILES,
	name			= "AGM_84H",
	user_name		= _("AGM-84H"),
	scheme			= "cruise_missile",
	class_name		= "wAmmunitionCruise",
	model			= "agm-84h",
	mass			= 675,
	
	wsTypeOfWeapon 	= {wsType_Weapon,wsType_Missile,wsType_AS_Missile,WSTYPE_PLACEHOLDER},

	Escort			= 0,
	Head_Type		= 5,
	sigma			= {20, 20, 20},
	M				= 675.0,
	H_max			= 13000.0,
	H_min			= -1,
	Diam			= 343.0,
	Cx_pil			= 8,
	D_max			= 1800000.0,
	D_min			= 10000.0,
	Head_Form		= 0,
	Life_Time		= 100000,
	Nr_max			= 6,
	v_min			= 170.0,
	v_mid			= 237.5,
	Mach_max		= 0.95,
	t_b				= 0.0,
	t_acc			= 5.0,
	t_marsh			= 10000.0,
	Range_max		= 2500000.0,
	H_min_t			= 500.0,
	Fi_start		= 0.35,
	Fi_rak			= 3.14152,
	Fi_excort		= 0.7,
	Fi_search		= 99.9,
	OmViz_max		= 99.9,
	X_back = -3.392,
	Y_back = 0.064,
	Z_back = 0.0,
	Reflection = 0.1691,
	KillDistance = 0.0,
	
	add_attributes = {"Cruise missiles"},
		
	shape_table_data =
	{
		{
			name	 = "AGM-84H",
			file	 = "agm-84h",
			life	 = 1,
			fire	 = { 0, 1},
			username = _("AGM-84H"),
			index	 = WSTYPE_PLACEHOLDER,
		},
	},
	
	controller = {
		boost_start	= 0.001,
		march_start = 0.8,
	},
	
	fm = {
		mass        = 675,  
		caliber     = 0.343,  
		cx_coeff    = {1, 0.3, 0.65, 0.018, 1.6},
		L           = 4.37,
		I           = 1500,
		Ma          = 3,	--y
		Mw          = 10,
		wind_sigma	= 0.0,
		wind_time	= 0.0,
		Sw			= 1.2,
		dCydA		= {0.07, 0.036},
		A			= 0.08,
		maxAoa		= 0.2,
		finsTau		= 0.08,
		Ma_x		= 3,
		Ma_z		= 3,
		Kw_x		= 0.05,
	},
	
	simple_seeker = {
		sensitivity = 0,
		delay		= 0.0,
		FOV			= 0.6,
		maxW		= 500,
		opTime		= 9999,
	},
	
	control_block ={
		seeker_activation_dist		= 20000,
		default_cruise_height		= 50,
		obj_sensor					= 1,
		can_update_target_pos		= 0,
		turn_before_point_reach		= 1,
		turn_hor_N					= 0.8,
		turn_max_calc_angle_deg		= 90,
		turn_point_trigger_dist		= 100,
	},
	
	final_autopilot =		{
		delay = 0,
		K					= 60,
		Ki					= 0,
		Kg					= 4,
		finsLimit			= 0.8,
		useJumpByDefault	= 1,
		J_Power_K			= 2.4,
		J_Diff_K			= 0.8,
		J_Int_K				= 0,
		J_Angle_K			= 0.17,
		J_FinAngle_K		= 0.195,
		J_Angle_W			= 2.4,
		hKp_err				= 100,
		hKp_err_croll		= 0.04,
		hKd					= 0.005,
		max_roll			= 0.7,
	},
	
	cruise_autopilot = {
		delay				= 1,
		Kp_hor_err			= 240,
		Kp_hor_err_croll	= 0.06,
		Kd_hor				= 0,
		Kp_ver				= 9,
		Kii_ver				= 0.2,
		Kd_ver				= 0,
		Kp_eng				= 265,
		Ki_eng				= 0.003,
		Kd_eng				= 0,
		Kp_ver_st1			= 0.009,
		Kd_ver_st1			= 0.015,
		Kp_ver_st2			= 0.00018,
		Kd_ver_st2			= 0.00005,
		
		auto_terrain_following			= 1,
		auto_terrain_following_height	= 50,
		
		alg_points_num			= 7,
		alg_calc_time			= 1.5,
		alg_vel_k				= 6,
		alg_div_k				= 2,
		alg_max_sin_climb		= 0.7,
		alg_section_temp_points	= 3,
		alg_tmp_point_vel_k		= 1.5,
		no_alg_vel_k			= 10,
		
		max_roll			= 0.7,
		max_start_y_vel		= 35,
		stab_vel			= 237.5,
		finsLimit			= 0.8,
		estimated_N_max		= 6,
		eng_min_thrust		= -100,
		eng_max_thrust		= 3000,		
	},
	
	boost = {	--	air launch - no booster
		impulse								= 0,
		fuel_mass							= 0,
		work_time							= 0,
		boost_time							= 0,
		boost_factor						= 0,
		nozzle_position						= {{0, 0, 0}},
		nozzle_orientationXYZ				= {{0, 0, 0}},
		tail_width							= 0,
		smoke_color							= {0.0, 0.0, 0.0},
		smoke_transparency					= 0.0,
		custom_smoke_dissipation_factor		= 0.0,				
	},
	
	booster_animation = {
		start_val = 0,
	},
	
	play_booster_animation = {
		val = 0,
	},
	
	march = {
		impulse			= 690,
		fuel_mass		= 67.5,
		work_time		= 9999,
		min_fuel_rate	= 0.005,
		min_thrust		= -100,
		max_thrust		= 3000,
		thrust_Tau		= 0.0017,
	},
	
	warhead		= penetrating_warhead(340, 343),
	warhead_air = penetrating_warhead(340, 343),
}

declare_weapon(AGM_84H)

declare_loadout({
	category 		= CAT_MISSILES,
	CLSID	 		= "{AGM_84H}",
	attribute		= AGM_84H.wsTypeOfWeapon,
	Count 			= 1,
	Cx_pil			= 0.0018,
	Picture			= "agm84a.png",
	displayName		= AGM_84H.user_name,
	Weight			= AGM_84H.mass,
	Elements  		= {{ShapeName = "agm-84h"}},
})

declare_loadout({
	category 		= CAT_MISSILES,
	CLSID	 		= "{AGM_84E}",
	attribute		= {wsType_Weapon,wsType_Missile,wsType_AS_Missile,63},
	Count 			= 1,
	Cx_pil			= 0.0018,
	Picture			= "agm84a.png",
	displayName		= _('AGM-84E SLAM'),
	Weight			= 628,
	Elements  		= {{ShapeName = "agm-84e"}},
})