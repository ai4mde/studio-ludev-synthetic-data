// @ts-check
import { beforeEach, describe, expect, test } from '@playwright/test';


describe('AI4MDE App Login', () => {
    test('webpage loads successfully', async ({ page }) => {
        await page.goto('http://ai4mde.localhost');
        await expect(page).toHaveTitle(/AI4MDE - Editor/);
    });
    test('can fill and submit login form', async ({ page }) => {
        await page.goto('http://ai4mde.localhost');
        await page.fill('input[name="username"]', 'admin');
        await page.fill('input[name="password"]', 'sequoias');
        await page.click('button[type="submit"]');
        await page.waitForLoadState('networkidle');
        await expect(page.locator('h1')).toHaveText('Welcome to AI4MDE Studio');
    });
});

describe('AI4MDE App Features', () => {
    beforeEach(async ({ page }) => {
        await page.goto('http://ai4mde.localhost');
        await page.fill('input[name="username"]', 'admin');
        await page.fill('input[name="password"]', 'sequoias');
        await page.click('button[type="submit"]');
        await page.waitForLoadState('networkidle');
        await expect(page.locator('h1')).toHaveText('Welcome to AI4MDE Studio');
    }); 
});
