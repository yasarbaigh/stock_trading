package org.baigh.nse.delivery;

import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import javax.imageio.ImageIO;

import org.apache.commons.io.FileUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.support.ui.Select;

import ru.yandex.qatools.ashot.AShot;
import ru.yandex.qatools.ashot.Screenshot;
import ru.yandex.qatools.ashot.coordinates.WebDriverCoordsProvider;
import ru.yandex.qatools.ashot.shooting.ShootingStrategies;

public class DeliveryQuantityCapture {
	
	public static long TIME_UNIT = 3000;
	
	public static void main(String[] args) throws Exception {

		//System.setProperty("webdriver.gecko.driver", "F:\\yasar\\my-git\\geckodriver-v0.24.0\\geckodriver.exe");
		
		System.setProperty("webdriver.gecko.driver", "/opt/jars/sel/geckodriver");

		final FirefoxOptions options = new FirefoxOptions();
		options.addArguments("--start-maximized", "--start-fullscreen");
		//options.setHeadless(true);

		final WebDriver driver = new FirefoxDriver(options);

		//driver.get("https://www.nseindia.com/products/content/equities/equities/eq_security.htm");
		
		System.out.println(System.currentTimeMillis());
		final String date = new SimpleDateFormat("yyyy-MM-dd").format(new Date());
		Thread.sleep(TIME_UNIT);
		new File(date).mkdirs();
		final String scripts = "ADANIPORTS,ASIANPAINT,BAJAJ-AUTO,BHARTIARTL,BPCL,BRITANNIA,CIPLA,COALINDIA,DRREDDY,EICHERMOT,GAIL,GRASIM,HCLTECH,HEROMOTOCO,HINDALCO,HINDUNILVR,INFRATEL,INFY,IOC,JSWSTEEL,LT,M&M,MARUTI,ONGC,POWERGRID,RELIANCE,SUNPHARMA,TATAMOTORS,TATASTEEL,TCS,TECHM,TITAN,ULTRACEMCO,UPL,VEDL,WIPRO";

		for (final String item : scripts.split(",")) {
			getDQ(driver, date, item);
		}

		driver.close();
		driver.quit();

	}

	private static void getDQ(WebDriver driver, String directoryValue, String script) throws Exception {
		driver.get("https://www.nseindia.com/products/content/equities/equities/eq_security.htm");
		Thread.sleep(TIME_UNIT);
		
		final Select dropdownSeries = new Select(driver.findElement(By.id("series")));
		dropdownSeries.selectByValue("EQ");


		driver.findElement(By.id("symbol")).clear();
		driver.findElement(By.id("symbol")).sendKeys(script);
		
		
		final Select dropdown = new Select(driver.findElement(By.id("dateRange")));

		// dropdown.selectByValue("15days");
		dropdown.selectByValue("1month");

		driver.findElement(By.className("getdata-button")).click();

		Thread.sleep(TIME_UNIT);

		takeFullPageScreenShotAsByte(driver, directoryValue, script);
	}

	private static void takeFullPageScreenShotAsByte(WebDriver webDriver, String directoryValue, String script)
			throws Exception {
		final Screenshot fpScreenshot = new AShot().shootingStrategy(ShootingStrategies.viewportPasting(1000))
				.takeScreenshot(webDriver);

		final BufferedImage originalImage = fpScreenshot.getImage();

		ImageIO.write(originalImage, "PNG", new File(directoryValue + File.separator + script + ".png"));

	}

	private static byte[] takeFullPageScreenShotAsByteArray(WebDriver webDriver, String directoryValue, String script)
			throws Exception {
		final Screenshot fpScreenshot = new AShot().shootingStrategy(ShootingStrategies.viewportPasting(1000))
				.takeScreenshot(webDriver);

		final BufferedImage originalImage = fpScreenshot.getImage();

		try (ByteArrayOutputStream baos = new ByteArrayOutputStream()) {
			ImageIO.write(originalImage, "png", baos);
			baos.flush();
			return baos.toByteArray();
		}

	}

	private void elementScreenCapture(WebDriver driver, String directoryValue, String script) throws IOException {

		final String fileName = directoryValue + File.separator + script + ".png";
		final WebElement webElement = driver.findElement(By.className("archives"));

		final Screenshot screenshot = new AShot().coordsProvider(new WebDriverCoordsProvider()).takeScreenshot(driver,
				webElement);
		ImageIO.write(screenshot.getImage(), "PNG", new File(fileName));
	}

	private void normalScreenCapture(WebDriver driver, String directoryValue, String script) throws Exception {

		final File scrFile = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
		FileUtils.copyFile(scrFile, new File(directoryValue + File.separator + script + ".png"));

	}

}
