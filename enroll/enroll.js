const puppeteer = require('puppeteer');
const config = require('./config.json');
var crnid = process.argv.slice(2);
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

async function report (log) {
	currentTime = new Date();
	console.log(currentTime.toString().split('G')[0] + ': ' + log)
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

async function run () {
	const browser = await puppeteer.launch({
        headless: false,
		product: 'chrome',
		defaultViewport: { width: 1500, height: 768 }})
	const page = await browser.newPage()
	await page.setCacheEnabled(false);
	
	await page.goto('https://sso.sis.gatech.edu/ssomanager/c/SSB' , {waitUntil: 'load' })
	await page.waitForSelector('#username')
	await page.type('#username', config.usern)
	await page.type('#password', config.userp)
	await page.waitForTimeout(1500)
	await page.click('#login > div.buttons.row.btn-row > input.button.btn-submit')
	await page.waitForTimeout(5000)
	await page.keyboard.press('Tab')
	await page.keyboard.press('Tab')
	await page.keyboard.press('Enter')
	while(true) {
		if (page.url().includes('bmenu.P_MainMnu')) {
			break
		}
		await page.waitForTimeout(2000)
	}
	await page.goto('https://oscar.gatech.edu/bprod/bwskfreg.P_AltPin')
	await page.waitForSelector('body > div.pagebodydiv > form > input[type=submit]')
	await page.click('body > div.pagebodydiv > form > input[type=submit]')
	await page.waitForSelector('#crn_id1')
	await page.type('#crn_id1', crnid)
	await page.waitForTimeout(1500)
	await page.waitForSelector('body > div.pagebodydiv > form > input[type=submit]:nth-child(28)')
	await page.click('body > div.pagebodydiv > form > input[type=submit]:nth-child(28)')
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

run();