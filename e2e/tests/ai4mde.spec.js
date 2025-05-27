// @ts-check
import { beforeEach, describe, expect, test } from '@playwright/test';

const login = async (page) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'sequoias');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
}

const navigateToProject = async (page) => {
    await page.goto('/projects/');
    await page.waitForLoadState('networkidle');
}

const selectProject = async (page, projectName = 'DemoProject') => {
    await page.locator('a[href*="/projects/"]').filter({ hasText: projectName }).click();
    await page.waitForLoadState('networkidle');
}

const selectSystem = async (page, systemName = 'DemoSystem') => {
    await page.locator('a[href*="/systems/"]').filter({ hasText: systemName }).click();
    await page.waitForLoadState('networkidle');
}

const navigateToPrototypes = async (page) => {
    await page.locator('a[href*="/systems/"]').filter({ hasText: 'Prototypes' }).click();
    await page.waitForLoadState('networkidle');
}

describe('AI4MDE App Features (Prerequisites)', () => {
    test('can fill and submit login form', async ({ page }) => {
        await login(page);
        await expect(page.getByRole('heading', { name: 'Welcome to AI4MDE Studio' })).toBeVisible();
    })
    test('can navigate to "Project"', async ({ page }) => {
        await login(page);
        await navigateToProject(page);
        await expect(page.getByRole('heading', { name: 'Projects' })).toBeVisible();
    });
    test('can navigate to "System"', async ({ page }) => {
        await login(page)
        await navigateToProject(page)
        await selectProject(page)
        await expect(page.getByRole('heading', { name: /Systems - Demo/ })).toBeVisible();
    });
    test('can navigate to "Diagram"', async ({ page }) => {
        await login(page);
        await navigateToProject(page);
        await selectProject(page);
        await selectSystem(page);
        await expect(page.getByRole('heading', { name: 'Class Diagram' })).toBeVisible();
        await expect(page.getByRole('heading', { name: 'Activity Diagram' })).toBeVisible();
        await expect(page.getByRole('heading', { name: 'Usecase Diagram' })).toBeVisible();
        await expect(page.getByRole('heading', { name: 'Component Diagram' })).toBeVisible();
    });
    test ('can navigate to "Prototypes"', async ({ page }) => {
        await login(page);
        await navigateToProject(page);
        await selectProject(page);
        await selectSystem(page);
        await navigateToPrototypes(page);
        await expect(page.getByRole('heading', { name: 'Prototypes' })).toBeVisible();
        await expect(page.getByRole('button', { name: 'Generate new prototype'})).toBeVisible();
    });
});

describe('AI4MDE App Features (Frontend UI)', () => {
    beforeEach(async ({ page }) => {
        await login(page);
        await navigateToProject(page);
        await selectProject(page);
        await selectSystem(page);
        await navigateToPrototypes(page);
        await expect(page.getByRole('heading', { name: 'Prototypes' })).toBeVisible();
        await expect(page.getByRole('button', { name: 'Generate new prototype'})).toBeVisible();
    });

    test('prototype generation modal appears', async ({ page }) => {
        await page.locator('button').filter({ hasText: 'Generate new prototype' }).click();
        await expect(page.getByRole('dialog')).toBeVisible();
        await expect(page.getByLabel('Name')).toBeVisible();
        await expect(page.locator('input[placeholder="Prototype"]')).toBeVisible();
        await expect(page.getByText('Use Synthetic Data')).toBeVisible(); 
        await expect(page.getByRole('switch', { name: 'Use Synthetic Data' })).toBeVisible();
        await expect(page.getByRole('button', { name: 'Create' })).toBeVisible();
    });

    test('synthetic data modal appears', async ({ page }) => {
        await page.locator('button').filter({ hasText: 'Generate new prototype' }).click();
        await page.getByRole('switch', { name: 'Use Synthetic Data' }).click();
        await expect(page.getByRole('dialog')).toBeVisible();
        await expect(page.getByRole('heading', { name: 'Specify Synthetic Data Amount Per Node' })).toBeVisible();
        await expect(page.getByLabel('Custom Instructions')).toBeVisible();
        await expect(page.locator('input[placeholder="e.g., 10 samples per user with real names"]')).toBeVisible();
        await expect(page.getByRole('button', { name: 'Done' })).toBeVisible();
    })
})

describe('AI4MDE App Features (Generation)', () => {
    beforeEach(async ({ page }) => {
        await login(page);
        await navigateToProject(page);
        await selectProject(page);
        await selectSystem(page);
        await navigateToPrototypes(page);
        const trashButtonCount = await page.locator('button:has(.lucide-trash)').count();
        if (trashButtonCount > 0) {
            await page.getByRole('button', { name: 'Delete all' }).click();
            await page.getByRole('button', { name: 'Confirm'}).click();
            await expect(page.locator('button:has(.lucide-trash)')).toHaveCount(0);
        }
        await page.locator('button').filter({ hasText: 'Generate new prototype' }).click();
        await expect(page.getByRole('dialog')).toBeVisible();
        await expect(page.locator('input[placeholder="Prototype"]')).toBeVisible();
    });

    test('can generate prototype without specific instructions', async ({ page }) => {
        await page.fill('input[placeholder="Prototype"]', 'DemoPrototype')
        await page.getByRole('switch', { name: 'Use Authentication' }).click();
        await page.getByRole('switch', { name: 'Use Synthetic Data' }).click();
        await page.keyboard.press('Escape');
        await page.getByRole('button', { name: 'Create' }).click();
        await expect(page.getByText('Generating')).toBeVisible();
        await expect(page.locator('.animate-spin')).toBeVisible();
        await expect(page.getByText('Generating')).not.toBeVisible({ timeout: 60000 }); // 1 minute
        await page.reload();
        await page.waitForLoadState('networkidle');
        await expect(page.getByText('DemoPrototype')).toBeVisible();
        await page.locator('button').filter({ hasText: 'Run' }).click();
        await expect(page.getByText('http://prototype.ai4mde.localhost')).toBeVisible({ timeout: 60000 });
    })

    test.only('can visit generated prototype', async ({ page }) => {
        await page.fill('input[placeholder="Prototype"]', 'DemoPrototype');
        await page.getByRole('switch', { name: 'Use Authentication' }).click();
        await page.getByRole('switch', { name: 'Use Synthetic Data' }).click();
        await page.keyboard.press('Escape');
        await page.getByRole('button', { name: 'Create' }).click();
        await expect(page.getByText('Generating')).not.toBeVisible({ timeout: 60000 });
        await page.reload();
        await page.waitForLoadState('networkidle');
        await page.locator('button').filter({ hasText: 'Run' }).click();
        await expect(page.getByText('http://prototype.ai4mde.localhost')).toBeVisible({ timeout: 60000 });
        await page.goto('http://prototype.ai4mde.localhost');
        await page.waitForLoadState('networkidle');
        await expect(page.getByRole('heading', { name: 'DemoPrototype prototype' })).toBeVisible();
        await expect(page.locator('a[href*="/DemoInterface/"]').filter({ hasText: 'DemoInterface' })).toBeVisible();
        await page.locator('a[href*="/DemoInterface/"]').filter({ hasText: 'DemoInterface' }).click();
        await expect(page).toHaveTitle('DemoInterface');
        await expect(page.getByRole('heading', { name: 'Welcome!' })).toBeVisible();
        await expect(page.locator('a[href*="/render_DemoInterface_"]').filter({ hasText: 'Cars' })).toBeVisible();
        await page.locator('a[href*="/render_DemoInterface_"]').filter({ hasText: 'Cars' }).click();
        await expect(page.getByRole('heading', { name: 'Cars' })).toBeVisible();
        await expect(page.locator('table')).toBeVisible();
        await expect(page.locator('th', { hasText: 'manufacturer' })).toBeVisible();
        await expect(page.locator('th', { hasText: 'model' })).toBeVisible();
        await expect(page.locator('th', { hasText: 'topSpeed' })).toBeVisible();
        await expect(page.locator('th', { hasText: 'fuel' })).toBeVisible();
        await expect(page.locator('table tr')).toHaveCount(11);
        const manufacturers = await page.locator('table tr:not(:first-child) td:first-child').allTextContents();
        expect(manufacturers.every(m => ['AUDI', 'BMW', 'MERCEDES'].includes(m.trim()))).toBe(true);
    });
})
