
describe('Hacker News登录测试', () => {
    it('登录页面', () => {
        cy.visit("https://news.ycombinator.com/login?goto=news")
        cy.get('input[name="acct"]').eq(0).type('test');
        cy.get('input[name="pw"]').eq(0).type('123456');
        cy.get('input[value="login"]').click();
        cy.get('body').should('contain', 'Bad login');
        cy.screenshot();
    })
})