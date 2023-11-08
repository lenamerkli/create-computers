package me.merkli.create_computers;

import com.simibubi.create.Create;

import com.simibubi.create.foundation.data.CreateRegistrate;

import com.simibubi.create.foundation.item.ItemDescription;

import com.simibubi.create.foundation.item.KineticStats;

import com.simibubi.create.foundation.item.TooltipHelper;
import com.simibubi.create.foundation.item.TooltipModifier;

import io.github.fabricators_of_create.porting_lib.util.EnvExecutor;
import me.merkli.create_computers.item.AllCreativeModeTabs;
import me.merkli.create_computers.item.AllItems;
import net.fabricmc.api.ModInitializer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CreateComputersMod implements ModInitializer {
	public static final String ID = "create_computers";
	public static final String NAME = "Create Computers";
	public static final Logger LOGGER = LoggerFactory.getLogger(NAME);
	public static final CreateRegistrate REGISTRATE = CreateRegistrate.create(ID);

	static {
		REGISTRATE.setTooltipModifierFactory(item -> new ItemDescription.Modifier(item, TooltipHelper.Palette.STANDARD_CREATE)
				.andThen(TooltipModifier.mapNull(KineticStats.create(item))));
	}

	@Override
	public void onInitialize() {
		LOGGER.info("Create addon mod [{}] is loading alongside Create [{}]!", NAME, Create.VERSION);
		LOGGER.info(EnvExecutor.unsafeRunForDist(
				() -> () -> "{} is accessing Porting Lib from the client!",
				() -> () -> "{} is accessing Porting Lib from the server!"
		), NAME);

		AllCreativeModeTabs.init();
		AllItems.register();

		REGISTRATE.register();

	}
}
